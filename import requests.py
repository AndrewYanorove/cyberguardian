import requests
import json
import time

# Отключаем SSL предупреждения
requests.packages.urllib3.disable_warnings()

# Ваш токен
ACCESS_TOKEN = "eyJjdHkiOiJqd3QiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiUlNBLU9BRVAtMjU2In0.bDpnmUJILoJzZkMohQd8UXR74gHgtjmW9xfVkjVqLEpqjDzGQ3VSIsmvRV4vV7MmOrOjlfHtNwoltNlZUR00q77jCKtYEfE8UDsRB8sef08qhbhEjvsietCyy6m42aQr1lMR_R8VB33bc25xJuQKmuDMHs0S56WlOFWZ3osYyT42y6533WSuXe8B8RpyuQW67mWLVfdv_1IV0AM3U4xsuWIUcidai_MAmib27D9WK7U_MdErjqtjb89iaczW-7I3gyL-bMlewHtUxYhWVrK3SQGtkfp9RXh12IQm2ieore9blRgShN2xgQ14KY7yxqYe081gAzMkTy_v1AOM2OkDtQ.aQuXTQAIVf5pMLjCu9-FGQ.lVA6oYqeUdJmIV8pUx9PtPiFSWYXUdqlZgX-fpvrARm6f4G406wrEvQHDc60AolHLXwMDuaJSLS7yG8gPjFS0RiQlfJRTCPWDK15RvnSkfVIJllvgzjdSxHSOs908U6AWqcNq9g82Eqr9X55gH9rIzERERkufFynA1fjTH3NKj51njRkv7cPw2iUo_sN0d33dhcSr9BJsww_76hxf_TkOWI132ItS6hWKMI8PzM4UeH7n7z0_R16O56uZZxgCcQX54PobmOQK3qcnn-1K-QDQ98pAKcoz-RvfDaSJZglnLT5-hEI8I2byFdPccGMHzpZrcNW5N9Jz3AlAYFSSYFEST2WczdhMfpbFnqwrsQ07-EZxg2R21jXFiKIAGiSTKXSLIuQgvtrLfO20VkQV9pbwmPjo7K-9bRG5F0vOniONBIlt3N2vNrUP62v3itd3f7_8FsfWXzEn3U3dXM88OMrx7PqzYJzWl4UHrGIcjhqXhOz5lwQvsYf9NH-Gh22-FtjSQdPhBPB1Gn4jGNx94rj9SoXWOUcqvE9nlYDHv1y_7hWVqjZlt7boVOD6GD2i_2cUd-HPWKAALvWA0hGegXQXNU1Z_g5akbOPx3YudHq-zxL4490jQOXsg4o4DMbLCp691mlPPQgL6f5R2Oc7i9PiDRQ2HxmfdUGGKzab6ddCEXGKVxwnzZ2mUz1EdnrfR5unqqFphUP0iugzIqp0Tn9-ShcoM1iyfy7Aq7Zww2s_lQ.sCz4Br1cYb4uqms0aiSl8B16Ev_sjY31Xv5NyJsYtWU"

def test_models_api():
    """Тестируем получение списка моделей"""
    url = "https://gigachat.devices.sberbank.ru/api/v1/models"
    
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print("Response:")
        
        if response.status_code == 200:
            models = response.json()
            print(json.dumps(models, indent=2, ensure_ascii=False))
            
            # Показываем доступные модели
            if 'data' in models:
                print(f"\n✅ Доступные модели:")
                for model in models['data']:
                    print(f"  - {model.get('id', 'Unknown')}")
        else:
            print(f"❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

def test_chat_api():
    """Тестируем чат API"""
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    
    payload = {
        "model": "GigaChat",
        "messages": [
            {
                "role": "system",
                "content": "Ты эксперт по кибербезопасности. Отвечай кратко и по делу."
            },
            {
                "role": "user",
                "content": "Привет! Расскажи в двух предложениях о важности кибербезопасности"
            }
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, verify=False, timeout=30)
        
        print(f"\n🤖 Тест чат API:")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content']
            print(f"✅ Ответ GigaChat: {answer}")
        else:
            print(f"❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

# Запускаем тесты
print("🧪 Тестируем GigaChat API...")
test_models_api()
test_chat_api()