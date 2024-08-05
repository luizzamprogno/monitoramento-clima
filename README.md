# Extração de dados climáticos

Esse projeto faz uma varredura e extrai dados climáticos do momento atual e uma previsão de 3 dias, do site https://www.tempo.com/, organiza as informações e faz o envio automático para um email.

## 🚀 Começando
### 📋 Pré-requisitos

```
Google Chrome
Chrome Web Driver
Senha de App do Google
```

Instalar as seguintes bibliotecas necessárias

* [selenium]('https://www.selenium.dev/')
* [schedule]('https://schedule.readthedocs.io/en/stable/)
* [webdriver-manager]('https://pypi.org/project/webdriver-manager/')


## ⚙️ Executando os testes

Para realizar testes, foi deixado como padrão, 5 segundos como período de repetição automática do código, mas a ideia para uma apliação real seria de período de 1 dia.
Para fazer isso, na função 'schedule_email', altere o método da biblioteca schedule de 'seconds' para 'days', e no momento da chamada da função 'schedule_email', altere o único parâmetro para 1. Isso vai fazer com que o email seja enviado uma vez por dia