### Для запуска приложения создайте и активируйте виртуальное окружение
```
python3 -m venv venv
source venv/bin/activate
```
### Возможно вам будет нужно установить переменную окружения
```
export PYTHONPATH=$PYTHONPATH:$(pwd)
```
### Установите необходимые быблиотеки
```
pip install -r requirements.txt
```
### Запустите скрипт
### python main.py -m месяц -y год -f формат 
```
python main.py -m 4 -y 2020 -f 640x480 
```

