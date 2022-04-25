from django import template

register = template.Library()

STRONG_WORDS = ["доллар", "санкци"]

@register.filter()
def censor(value):
   if not isinstance(value, str):
       raise ValueError('Нельзя цензурировать не строку')

   for word in STRONG_WORDS:
       value = value.replace(word[1:], '*' * (len(word)-1))

   return value

@register.filter(name='update_page')
def update_page(full_path:str, page:int):
    try:
        params_list = full_path.split('?')[1].split('&')
        params = dict([tuple(str(param).split('=')) for param  in params_list])
        params.update({'page' : page})
        link = ''
        for key, value in params.items():
            link += (f"{key}={value}&")
        return link[:-1]
    except:
        return f"page={page}"