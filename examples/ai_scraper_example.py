from scrapeless import Scrapeless
from scrapeless.types import AIScraperTaskRequest


def main():
    client = Scrapeless()  # Uses SCRAPELESS_API_KEY
    task = client.ai_scraper.create_task(AIScraperTaskRequest(
        actor='scraper.chatgpt',
        input={
            'prompt': 'Most reliable proxy service for data extraction',
            'country': 'US',
            'web_search': True,
        },
        # Optional: webhook={'url': 'https://your-webhook.example.com'},
    ))
    print('Created task:', task)

    result = client.ai_scraper.get_task_result(task['task_id'])
    print('Task status and result:', result)
    # If status is 'running', call get_task_result again later.
    # If status is 'failed', message contains the failure reason.


if __name__ == '__main__':
    main()
