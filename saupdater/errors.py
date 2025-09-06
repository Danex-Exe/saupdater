from .logger import Logger


# Настройка логгера для ошибок
error_logger = Logger(title="SAUPDATER-ERROR", log_file="saupdater_errors.log")


class UpdaterError(Exception):
    """Базовое исключение для всех ошибок библиотеки."""
    def __init__(self, message: str, code: int = 1000):
        self.message = message
        self.code = code
        super().__init__(f"UPDATER-{code}: {message}")
        error_logger.error(f"{self.__class__.__name__}: {message} (code: {code})")


# ===== Ошибки операций =====
class OperationError(UpdaterError):
    """Ошибки выполнения операций обновления"""
    def __init__(self, message: str, operation: str = None):
        super().__init__(f"Operation failed: {message}", 2000)
        self.operation = operation

class GetGitHubVersionError(OperationError):
    """Ошибка при получении версии репозитория"""
    def __init__(self, url: str):
        super().__init__(f"Error getting current version of github repository. Check if link {url} is correct")
        self.url = url

class GetLocalVersionError(OperationError):
    """Ошибка при получении локальной версии репозитория"""
    def __init__(self, version_file_path: str):
        super().__init__(f"Error getting current version of local repository. Check {version_file_path}")
        self.version_file_path = version_file_path

class LocalVersionNotFoundError(OperationError):
    """Ошибка не существующей локальной версии"""
    def __init__(self, local_version: str, link: str):
        super().__init__(f"Local version {local_version} is not one of the versions of repository {link}")
        self.local_version = local_version
        self.link = link

class RemoteOriginNotFoundError(OperationError):
    """Ошибка наличия remote origin"""
    def __init__(self):
        super().__init__(f"To use the module, you must link it to the GitHub repository.")

class GitPullError(OperationError):
    """Ошибка при git pull"""
    def __init__(self, error: str):
        super().__init__(f"An error occurred while using the git pull command\n{error}")


# ===== Ошибки данных =====
class DataError(UpdaterError):
    """Ошибки обработки данных"""
    def __init__(self, message: str, data: any = None):
        super().__init__(f"Data error: {message}", 4000)
        self.data = data

class LinkError(DataError):
    """Ошибка формата ссылки"""
    def __init__(self, link: str, format_link):
        super().__init__(f"Invalid link format {link}\nUse {format_link}")
        self.link = link
        self.format_link = format_link

class LocalVersionError(DataError):
    """Ошибка формата локальной версии"""
    def __init__(self, version_file_path: str, version: str):
        super().__init__(f"Error getting current version of local repository. Check format version {version_file_path} - {version}")
        self.version_file_path = version_file_path
        self.version = version