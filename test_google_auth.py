from google_auth import GoogleAuth

desired_caps = {
    'platformName': 'Android',
    'appium:deviceName': 'Android Emulator',
    'appium:appPackage': 'com.google.android.gm',
    'appium:appActivity': '.ConversationListActivityGmail',
    'appium:automationName': 'UiAutomator2',
    'appium:platformVersion': '15.0',
    'appium:newCommandTimeout': 600,
    'noReset': False,
    'fastReset': True,
}

auth = GoogleAuth(desired_caps)

try:
    auth.login('your-email@gmail.com', 'your-password')  # noqa: Hardcoded credentials
finally:
    print('До новых встреч!')
