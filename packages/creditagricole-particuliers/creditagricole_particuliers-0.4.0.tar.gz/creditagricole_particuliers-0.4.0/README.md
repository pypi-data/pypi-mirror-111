# Client Python pour la banque Crédit agricole - Particuliers

![](https://github.com/dmachard/creditagricole_particuliers/workflows/Publish%20to%20PyPI/badge.svg)

Ce client Python est à destination des particuliers souhaitant récupérer ses opérations bancaires stockées par le Crédit Agricole.

## Installation

```python
pip install creditagricole_particuliers
```
  
## Authentification

```python
from creditagricole_particuliers import Authenticator

session = Authenticator(username="<n° de compte bancaire>", password=[1, 2, 3, 4, 5, 6], region="normandie")
```

## Lister l'ensemble des comptes bancaires

```python
from creditagricole_particuliers import Authenticator, Accounts

session = Authenticator(username="<n° de compte bancaire>", password=[1, 2, 3, 4, 5, 6], region="normandie")
accounts = Accounts(session=session)
for acc in accounts:
    print(acc)
```

Format JSON:

```python
accounts = Accounts(session=session)
print(accounts.as_json())
```

## Rechercher un compte bancaire

```python
from creditagricole_particuliers import Authenticator, Accounts

session = Authenticator(username="<n° de compte bancaire>", password=[1, 2, 3, 4, 5, 6], region="normandie")
account = Accounts(session=session).search(num="<n° de compte bancaire>")
print(account)
```

Format JSON:

```python
account = Accounts(session=session).search(num="<n° de compte bancaire>")
print(account.as_json())
```

## Récupération du solde d'un compte


```python
from creditagricole_particuliers import Authenticator, Accounts

session = Authenticator(username="<n° de compte bancaire>", password=[1, 2, 3, 4, 5, 6], region="normandie")
account = Accounts(session=session).search(num="<n° de compte bancaire>")
print(account.get_solde())
```

exemple pour la totalité des comptes


```python
from creditagricole_particuliers import Accounts

solde = Accounts(session=session).get_solde()
print(solde)
```


## Récupération des opérations bancaires

Exemple pour récupérer les 30 dernières opérations

```python
from creditagricole_particuliers import Authenticator, Accounts

# make auth
session = Authenticator(username="<n° de compte bancaire>", password=[1, 2, 3, 4, 5, 6], region="normandie")

# search account
account = Accounts(session=session).search(num="<n° de compte bancaire>")

# get operations
operations = account.operations(count=30)
for op in operations:
    print(operations)
```

Format JSON et filtrage par date

```python
account = Accounts(session=session).search(num="<n° de compte bancaire>")
operations = account.operations(date_start="2021-06-15", date_stop="2021-06-30", count=30)
print(operations.as_json())
```