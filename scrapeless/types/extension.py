from dataclasses import dataclass

@dataclass
class UploadExtensionResponse:
    extensionId: str
    name: str
    createdAt: str
    updatedAt: str

@dataclass
class ExtensionListItem:
    extensionId: str
    name: str
    version: str
    createdAt: str
    updatedAt: str

@dataclass
class ExtensionDetail:
    extensionId: str
    teamId: str
    manifestName: str
    name: str
    version: str
    createdAt: str
    updatedAt: str