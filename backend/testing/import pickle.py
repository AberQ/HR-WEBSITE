import pickle

# Это ваша байтовая строка
serialized_data = b"\x80\x04\x95$\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x02id\x94K\x01\x8c\x04name\x94\x8c\x0e\xd0\xa0\xd1\x83\xd1\x81\xd1\x81\xd0\xba\xd0\xb8\xd0\xb9\x94u."

# Десериализация данных
try:
    data = pickle.loads(serialized_data)
    print(data)
except pickle.UnpicklingError as e:
    print(f"Ошибка при десериализации: {e}")
