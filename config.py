import os

from dotenv import load_dotenv

load_dotenv()

# Токен Telegram бота
BOT_TOKEN = os.getenv('BOT_TOKEN')

# API для получения файлов из Telegram
TELEGRAM_FILE_API_PATH = os.getenv('TELEGRAM_FILE_API')
TELEGRAM_FILE_API_URL = "{telegram_file_api_path}{bot_token}/{file_path}"

# Путь к файлу для хранения логов
LOGGER_PATH = os.getenv('LOGGER_PATH')

# HOST Барс-Офиса
HOST_BO = os.getenv('HOST_BO')

# API БО для получения учетной записи
GET_ACCOUNT_PATH = os.getenv('GET_ACCOUNT')
GET_ACCOUNT_URL = f"{HOST_BO}{GET_ACCOUNT_PATH}"

# API БО для регистрации Telegram аккаунта в БО
TELEGRAM_REGISTER_PATH = os.getenv('TELEGRAM_REGISTER')
TELEGRAM_REGISTER_URL = f"{HOST_BO}{TELEGRAM_REGISTER_PATH}"

# API БО для получения пароля от архива VPN
GET_VPN_PASSWORD_PATH = os.getenv('GET_VPN_PASSWORD')
GET_VPN_PASSWORD_URL = f"{HOST_BO}{GET_VPN_PASSWORD_PATH}"

# API БО для получения согласия на передачу данных через Telegram
GET_ACCOUNT_PAYSHEET_PATH = os.getenv('GET_ACCOUNT_PAYSHEET')
GET_ACCOUNT_PAYSHEET_URL = f"{HOST_BO}{GET_ACCOUNT_PAYSHEET_PATH}"

# API БО для получения расчетного листа
GIVE_PAYSHEET_PATH = os.getenv('GIVE_PAYSHEET')
GIVE_PAYSHEET_URL = f"{HOST_BO}{GIVE_PAYSHEET_PATH}"

# API БО для получения периода работы сотрудника
GET_EMPLOYEE_WORK_PERIOD_PATH = os.getenv('GET_EMPLOYEE_WORK_PERIOD')
GET_EMPLOYEE_WORK_PERIOD_URL = f"{HOST_BO}{GET_EMPLOYEE_WORK_PERIOD_PATH}"

# API БО для получения информации о сотруднике
GET_EMPLOYEE_INFO_PATH = os.getenv('GET_EMPLOYEE_INFO')
GET_EMPLOYEE_INFO_URL = f"{HOST_BO}{GET_EMPLOYEE_INFO_PATH}"

# API БО для получения фотографии сотрудника
GET_EMPLOYEE_PHOTO_PATH = os.getenv('GET_EMPLOYEE_PHOTO')
GET_EMPLOYEE_PHOTO_URL = f"{HOST_BO}{GET_EMPLOYEE_PHOTO_PATH}"

# API БО для изменения фотографии сотрудника
UPDATE_EMPLOYEE_PHOTO_PATH = os.getenv('UPDATE_EMPLOYEE_PHOTO')
UPDATE_EMPLOYEE_PHOTO_URL = f"{HOST_BO}{UPDATE_EMPLOYEE_PHOTO_PATH}"

# Логин и пароль integrator-а для авторизации при использовании API БО
INTEGRATOR_LOGIN = os.getenv('INTEGRATOR_LOGIN')
INTEGRATOR_PASSWORD = os.getenv('INTEGRATOR_PASSWORD')

# Confluence
CONFLUENCE = os.getenv('CONFLUENCE')

# URL для шаблонов приложений
APPLICATION_TEMPLATES = os.getenv('APPLICATION_TEMPLATES')
APPLICATION_TEMPLATES_URL = f"{CONFLUENCE}{APPLICATION_TEMPLATES}"

# URL для профессиональных сообществ
PROFESSIONAL_COMMUNITIES = os.getenv('PROFESSIONAL_COMMUNITIES')
PROFESSIONAL_COMMUNITIES_URL = f"{CONFLUENCE}{PROFESSIONAL_COMMUNITIES}"

# URL для интересных сообществ
INTEREST_COMMUNITIES = os.getenv('INTEREST_COMMUNITIES')
INTEREST_COMMUNITIES_URL = f"{CONFLUENCE}{INTEREST_COMMUNITIES}"

# URL для корпоративного университета
CORPORATE_UNIVERSITY = os.getenv('CORPORATE_UNIVERSITY')
CORPORATE_UNIVERSITY_URL = f"{CONFLUENCE}{CORPORATE_UNIVERSITY}"

# URL для отдела коммуникаций
COMMUNICATIONS_DEPARTMENT = os.getenv('COMMUNICATIONS_DEPARTMENT')
COMMUNICATIONS_DEPARTMENT_URL = f"{CONFLUENCE}{COMMUNICATIONS_DEPARTMENT}"

# URL для DMS
DMS = os.getenv('DMS')
DMS_URL = f"{CONFLUENCE}{DMS}"

# URL для реферальной программы
REFERRAL_PROGRAM = os.getenv('REFERRAL_PROGRAM')
REFERRAL_PROGRAM_URL = f"{CONFLUENCE}{REFERRAL_PROGRAM}"

# JIRA
JIRA = os.getenv('JIRA')
JIRA_BP = os.getenv('JIRA_BP')

# API для согласования БП "Командировка"
JIRA_ISSUE = os.getenv('JIRA_ISSUE')
JIRA_TRANSITIONS_URL = "{jira_bp}{jira_issue}{issuekey}/transitions"

# Справка с места работы
WORK_CERTIFICATE = os.getenv('WORK_CERTIFICATE')
WORK_CERTIFICATE_URL = f"{JIRA}{WORK_CERTIFICATE}"

# Трудовой договор
EMPLOYMENT_CONTRACT = os.getenv('EMPLOYMENT_CONTRACT')
EMPLOYMENT_CONTRACT_URL = f"{JIRA}{EMPLOYMENT_CONTRACT}"

# Трудовая книжка
WORK_BOOK = os.getenv('WORK_BOOK')
WORK_BOOK_URL = f"{JIRA}{WORK_BOOK}"

# Военный билет
MILITARY_REQUEST = os.getenv('MILITARY_REQUEST')
MILITARY_REQUEST_URL = f"{JIRA}{MILITARY_REQUEST}"

# ID чата в котором проходит модерация новых фото пользователей
APPROVE_PHOTO_CHAT_ID = os.getenv('APPROVE_PHOTO_CHAT_ID')
