import pickle

# Это ваша байтовая строка
serialized_data = b""

# Десериализация данных
try:
    data = pickle.loads(serialized_data)
    print(data)
except pickle.UnpicklingError as e:
    print(f"Ошибка при десериализации: {e}")
