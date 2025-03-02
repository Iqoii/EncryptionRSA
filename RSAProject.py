#Projet, encryption RSA sur python:
import random                         #On utilise la biblothèques random

def isPrime(n):                       #Vérifier si un nombre n est premier ou pas
    for i in range(2,int(n**0.5)+1):  #Boucle allant de 2, jusqu'à sqrt(n) + 1
        if n%i==0:                    #Calculer le reste de la division eucledienne de n par la variable d'itération i
            return False
    return True

def pgdc(p,q):                        # Fonction pour calculer le plus grand commun diviseur (PGDC) de deux nombres
    while q != 0:
        p, q = q, p%q
    return p

def extended_gcd(a, b):               # Fonction pour calculer deux nombres c et d tel que cx + dy = pgdc(a, b), merci StackOverflow!
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def modinv(a, m):                     #Fonction pour calculer l'inverse modulaire de a pour la multiplication modulo n (Cf.: https://fr.wikipedia.org/wiki/Inverse_modulaire)
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception("Modular inverse does not exist")
    else:
        return x % m

def find_public_exponent(t):          #Fonction pour calculer la clef publique d'encodage, 65,537 est souvent utilisé car il est le nombre de Fermat (F(n) = 2^(2n) + 1 avec n = 4) et sert à optimiser le code
  for i in range(2, t):
        if pgdc(i, t) == 1:           #On cherche un nombre plu petit que t mais "coprime" à celui-ci (Cf.: https://fr.wikipedia.org/wiki/Nombres_premiers_entre_eux)
            e = i
            break
  return e

def find_priv_exponent(t, e):         #Fonction pour calculer la clef privée de décodage
  j = 0
  while True:
      if (j * e) % t == 1:            #On essaye différentes valeurs de j jusqu'à ce que la condition (j * e) % t == 1 soit vraie, ce calcul revient à faire le modinv() de (j*e) modulo t mais je ne suis pas sûr
          d = j
          break
      j += 1
  return d

def keyGeneration():                   #Fonction pour regrouper les autres fonction dans une seule et déterminer les nombres premiers p et q ainsi que leur produit
  primes = [i for i in range(2,1000) if isPrime(i)]

  p = primes.pop(random.randint(0, len(primes)))
  q = random.choice(primes)
  n = p*q

  pub_exp = find_public_exponent((p-1)*(q-1))   #On utilise (p-1)*(q-1), la fonction indicatrice d'Euler (Merci Euler) (Cf. https://fr.wikipedia.org/wiki/Indicatrice_d%27Euler)

  priv_exp = find_priv_exponent((p-1)*(q-1), pub_exp)

  print("pub", pub_exp, "priv", priv_exp)

  return (n, priv_exp), (n, pub_exp)

private, public = keyGeneration()


def string_to_int(chaine):            #Fonction basique de décodage pour returner les mots en langage lisible
  chaine = list(chaine)
  code = []
  for i in range(len(chaine)):
    code.append(ord(chaine[i]))

  return code

def int_to_string(code):              #Fonction basique d'encodage pour donner la valeur UTF-8 de chacun des caractères
  chaine = []
  for i in range(len(code)):
    chaine.append(chr(code[i]))
  return chaine

def encrypt(message, public):           #Fonction d'encodage
  message = string_to_int(message)
  msg_number = []
  for element in message:
    msg_number.append((element**public[1]) % public[0])
  return msg_number


def decrypt(message_coded, private):    #Fonction de décodage
  message = []
  for element in message_coded:
    message.append((element**private[1]) % private[0])
  return "".join(int_to_string(message))


print("Encodage RSA:    ")
msg = str(input("\n Message à encrypter: "))

msg = encrypt(msg, public)

print("\n Message encrypté: \n", msg, "\n", int_to_string(msg))

print("\n Message:", decrypt(msg, private))


