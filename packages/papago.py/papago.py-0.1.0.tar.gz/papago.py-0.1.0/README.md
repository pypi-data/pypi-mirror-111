# papago.py
파이썬 네이버 파파고 API

## Install
```shell
pip isntall papago.py
```

## Usage
```python
import papago

p = papago.Papago('YOUR_CLIENT_ID', 'YOUR_CLIENT_SECRET')
```

### Translation
```python
p.translation('text', 'source', 'target')
```

### DetectLang
```python
p.detect_lang('text')
```

### DetectTranslation
```python
p.detect_translation('text', 'target')
```

### Romanization
```python
p.romanization('name')
```
