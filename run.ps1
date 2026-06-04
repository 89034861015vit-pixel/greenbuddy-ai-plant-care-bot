param(
  [string]$TelegramBotToken = $env:TELEGRAM_BOT_TOKEN,
  [string]$ProxyApiKey = $env:PROXYAPI_KEY
)

# Всегда даём возможность вставить значения вручную.
# Если просто нажать Enter — используем то, что было в окружении.
$inputToken = Read-Host "Enter TELEGRAM_BOT_TOKEN (Enter = use env)"
if ($inputToken) { $TelegramBotToken = $inputToken }

$inputKey = Read-Host "Enter PROXYAPI_KEY (Enter = use env)"
if ($inputKey) { $ProxyApiKey = $inputKey }

$TelegramBotToken = ("" + $TelegramBotToken).Trim()
$ProxyApiKey = ("" + $ProxyApiKey).Trim()

# Частая ошибка при вставке: пробелы/переносы строк. Telegram-токен не может содержать whitespace.
$TelegramBotToken = $TelegramBotToken -replace '\s', ''
$ProxyApiKey = $ProxyApiKey -replace '\s', ''

if (-not $TelegramBotToken) {
  Write-Error "Missing TELEGRAM_BOT_TOKEN."
  exit 1
}

if (-not $ProxyApiKey) {
  Write-Error "Missing PROXYAPI_KEY."
  exit 1
}

# Базовая проверка формата токена, чтобы сразу подсказать про неверную вставку.
if ($TelegramBotToken -notmatch '^\d+:[A-Za-z0-9_-]{20,}$') {
  Write-Error "TELEGRAM_BOT_TOKEN выглядит неверно. Вставь токен от @BotFather без пробелов."
  exit 1
}

$env:TELEGRAM_BOT_TOKEN = $TelegramBotToken
$env:PROXYAPI_KEY = $ProxyApiKey

python -u -m src.main

