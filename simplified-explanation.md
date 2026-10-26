# BB84 explicado como si tuvieras 8 años

*La criptografía cuántica sin matemáticas que asusten. Si puedes
explicárselo a un niño, puedes explicarlo en una entrevista.*

---

## 🕵️ Capítulo 1: El problema de los espías

Tú y tu amigo quieren inventar una **clave secreta**: una contraseña
que solo ustedes dos sepan. El problema: tienen que ponérsela de
acuerdo *hablando por teléfono*, y hay un espía escuchando todo. 📞👂

Con códigos normales, el espía puede copiar la clave sin que nadie se
dé cuenta. Con **criptografía cuántica**, si el espía escucha… **se
nota**. Es como un sello de cera en una carta: si alguien la abrió, el
sello está roto. Solo que aquí el "sello" lo ponen las leyes de la
física, y nadie las puede engañar.

> 🧒 *"¿Y cómo funciona?"*
> Con monedas girando, como las del laboratorio anterior. 🪙

---

## 📬 Capítulo 2: El juego de las dos cajas

Alice (tú) quiere mandarle bits a Bob (tu amigo) usando qubits. Inventan
un juego con **dos formas de mirar** la moneda:

- **Caja Z:** miras la moneda normal → ves cara (0) o sello (1).
- **Caja X:** la miras con unos lentes mágicos → también ves 0 o 1,
  pero es *otra* forma de mirar.

La regla de oro del juego: **si miras con la caja equivocada, lo que
ves es aleatorio**. Solo si usas la misma caja con la que Alice preparó
la moneda, ves el valor correcto.

Alice, por cada bit, elige al azar: qué valor (0 o 1) y qué caja (Z o X).
Bob, por cada moneda que llega, elige al azar con qué caja mirar.

> 🧒 *"¿Y si Bob usa la caja equivocada?"*
> Ve basura aleatoria. Pero no pasa nada, porque después lo arreglan…

---

## 🗣️ Capítulo 3: La llamada telefónica (que el espía sí puede oír)

Después de mandar todas las monedas, Alice y Bob **se llaman por
teléfono**: y el espía puede escuchar todo, no importa. Solo se dicen
una cosa: *"¿qué caja usaste en cada moneda?"*. Nunca dicen los valores.

Donde usaron la **misma caja** → se quedan con esos bits. ✅
Donde usaron cajas distintas → los tiran a la basura. 🗑️

Como cada uno eligió al azar, coinciden más o menos **la mitad** de las
veces. De 2000 monedas salen ~1000 bits buenos. A eso le dicen **sifting**
(cernir, como con un colador).

---

## 🔍 Capítulo 4: Atrapando al espía

Antes de usar la clave, sacrifican un pedacito: eligen ~20% de los bits
al azar y **los dicen en voz alta** por teléfono. Comparan:

- Sin espía: todos coinciden. Errores: **~0%**. 🎉
- Con espía: ¡1 de cada 4 está mal! Errores: **~25%**. 🚨

¿Por qué 25%? La espía Eve tiene que *mirar* cada moneda para copiarla,
y al mirar con la caja equivocada (la mitad de las veces) **rompe** la
moneda: la deja girando al azar. Cuando Bob la mira con la caja correcta,
la mitad de esas veces ve el valor incorrecto. Mitad de mitad = un
cuarto = 25%.

Al ver 25%, Alice y Bob dicen: *"esta clave está contaminada"* y **la
tiran completa**. El espía no se llevó nada útil, y ellos lo saben.

> 🧒 *"¿O sea que el espía nunca puede espiar en secreto?"*
> ¡Exacto! Esa es toda la magia: en el mundo cuántico, **espiar deja
> huellas**. En el mundo normal, no.

---

## 🧮 Capítulo 5: ¿Cuánto cuesta la seguridad?

De 2000 monedas crudas:
- ~1000 sobreviven al colador (misma caja)
- ~200 se sacrifican para buscar espías
- **~800 bits de clave secreta final**

O sea: la seguridad perfecta cuesta ~60% de los bits. Barato, para lo
que compra: una clave que **la física garantiza** que nadie copió en
secreto.

---

## ▶️ Cómo correrlo

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
bash run_all.sh
```

Verás el intercambio limpio (QBER 0.00%), el ataque de Eve (QBER ~25%
y el ABORTO), y la tablita de rendimiento. 🎉
