import re

alpha = 'alpha: my day was great! i got to eat some food. #grateful #amazing #wow #life'


list = re.split('[:#]', alpha)

print list
