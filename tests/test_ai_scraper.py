import copy
import unittest
from unittest.mock import Mock, patch

from scrapeless import Scrapeless, ScrapelessError
from scrapeless.types import AIScraperTaskRequest, ScrapingTaskRequest


class AIScraperTests(unittest.TestCase):
    def setUp(self):
        self.client = Scrapeless({
            'api_key': 'test-key',
            'base_api_url': 'https://api.example.com',
            'timeout': 1234,
        })
        patcher = patch('scrapeless.services.base.requests.request')
        self.request = patcher.start()
        self.addCleanup(patcher.stop)

    def respond(self, data, status=200):
        self.request.return_value = Mock(
            ok=200 <= status < 300,
            status_code=status,
            headers={'Content-Type': 'application/json'},
            json=Mock(return_value=data),
        )

    def test_create_task(self):
        for webhook in (None, {'url': 'https://callback.example.com', 'extra': True}):
            with self.subTest(webhook=webhook):
                self.request.reset_mock()
                input_data = {'prompt': 'test', 'nested': {'models': ['a', 'b']}}
                request = AIScraperTaskRequest('scraper.future-model', input_data, webhook)
                original = copy.deepcopy(request)
                response = {'task_id': 'task-1', 'status': 'running', 'data': {'retained': True}, 'extra': 42}
                self.respond(response, 201)
                self.assertEqual(self.client.ai_scraper.create_task(request), response)
                body = {'actor': 'scraper.future-model', 'input': input_data}
                if webhook is not None:
                    body['webhook'] = webhook
                self.request.assert_called_once_with(
                    'POST', 'https://api.example.com/api/v2/scraper/request',
                    headers={'Content-Type': 'application/json', 'X-API-Key': 'test-key', 'x-api-token': 'test-key'},
                    timeout=1.234, json=body,
                )
                self.assertEqual(request, original)

    def test_dictionary_parameters_are_forwarded_unchanged(self):
        payload = {'actor': 'scraper.chatgpt', 'input': {'prompt': 'test'}, 'custom': 42, 'webhook': None}
        original = copy.deepcopy(payload)
        self.respond({'task_id': 'task-1', 'status': 'success', 'task_result': ['answer']})
        self.client.ai_scraper.create_task(payload)
        self.assertEqual(self.request.call_args.kwargs['json'], original)
        self.assertEqual(payload, original)

    def test_get_task_result(self):
        for response in (
            {'status': 'running'},
            {'status': 'success', 'task_result': {'markdown': 'answer', 'citations': [{'url': 'https://example.com'}]}},
            {'status': 'failed', 'message': 'Model unavailable'},
        ):
            with self.subTest(status=response['status']):
                self.request.reset_mock()
                self.respond(response)
                self.assertEqual(self.client.ai_scraper.get_task_result('task /?#'), response)
                self.request.assert_called_once_with(
                    'GET', 'https://api.example.com/api/v2/scraper/result/task%20%2F%3F%23',
                    headers={'Content-Type': 'application/json', 'X-API-Key': 'test-key', 'x-api-token': 'test-key'},
                    timeout=1.234,
                )

    def test_http_error(self):
        self.respond({'message': 'Invalid token'}, 401)
        with self.assertRaises(ScrapelessError):
            self.client.ai_scraper.get_task_result('task-1')

    def test_transport_error(self):
        self.request.side_effect = ConnectionError('connection failed')
        with self.assertRaises(ScrapelessError):
            self.client.ai_scraper.get_task_result('task-1')

    def test_legacy_services_remain_available(self):
        self.respond({'taskId': 'old-task'}, 201)
        result = self.client.scraping.create_task(ScrapingTaskRequest('scraper.google.search', {'q': 'test'}))
        self.assertEqual(result, {'data': {'taskId': 'old-task'}, 'status': 201})
        self.assertEqual(self.request.call_args.args, ('POST', 'https://api.example.com/api/v1/scraper/request'))
        self.assertTrue(self.request.call_args.kwargs['json']['async'])
        self.assertNotIn('x-api-token', self.request.call_args.kwargs['headers'])
        self.assertTrue(callable(self.client.actor.run))
        self.assertIsNotNone(self.client.storage)


if __name__ == '__main__':
    unittest.main()
