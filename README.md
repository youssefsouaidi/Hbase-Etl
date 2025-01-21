

## Objectif

L'objectif de cet atelier est de concevoir une architecture moderne et scalable pour :
- Consommer des flux de données en temps réel depuis une API.
- Transformer ces données.
- Les stocker efficacement dans une base HBase.
- Les gérer via des opérations CRUD (Create, Read, Update, Delete).

Les technologies clés utilisées sont **Kafka** et **HBase**.

---

## Prérequis

### Environnement Docker
1. Créez un fichier `docker-compose.yml` pour orchestrer les services nécessaires :
   - **Zookeeper**
   - **Kafka**
   - **HBase**

2. Démarrez les conteneurs avec la commande :
   ```bash
   docker-compose up
   ```

### Présentation des Ports
- Kafka : `9092`
- HBase : `16010`, `9090`
- Zookeeper : `2181`

---

## API Utilisée : Random User Generator

**Random User Generator** est une API open-source permettant de générer des profils utilisateurs fictifs. Elle est utilisée pour :
- Tester des applications sans utiliser de vraies données personnelles.
- Simuler des scénarios d'utilisation pour des démos ou des outils d'apprentissage.

Lien : [Random User Generator](https://randomuser.me)

---

## Étapes de l'Atelier

### 1. Producteur Kafka

Un script Python est utilisé pour :
- **Récupérer les données utilisateur** depuis l'API Random User Generator.
- **Transformer** les données au format JSON.
- **Envoyer** les données transformées à un topic Kafka nommé `userdata`.

Bibliothèques utilisées :
- `uuid` : Génération d'identifiants uniques.
- `json` : Gestion du format JSON.
- `requests` : Requêtes HTTP vers l'API.
- `KafkaProducer` : Envoi des messages à Kafka.

### 2. Table HBase

Créez une table `userdata` dans HBase avec :
- **Trois familles de colonnes** : `address`, `contact`, et `info`.
- **Support de versions multiples** (par défaut : 3 versions par colonne).

### 3. Consommateur Kafka et Stockage HBase

Un consommateur Kafka est configuré pour :
- Lire les messages du topic `userdata`.
- Transformer et insérer les données reçues dans la table HBase.

---

## Fonctionnement du Pipeline

1. Le **producteur Kafka** récupère et envoie les données utilisateur en temps réel.
2. Le **consommateur Kafka** lit les messages et les insère dans HBase.
3. Les logs confirment la bonne insertion des données dans HBase.

---

## CRUD avec HBase

L'atelier inclut également des opérations CRUD pour manipuler les données stockées dans HBase.

---

## Résultats Attendus

À la fin de l'atelier, vous aurez mis en place un pipeline complet capable de :
- Consommer des données en temps réel.
- Transformer ces données.
- Les stocker dans une base structurée.
- Les gérer via des opérations CRUD.

---

Pour toute question ou assistance, n'hésitez pas à contacter les encadrants via [LinkedIn](https://ma.linkedin.com/in/youssef-souaidi-64371b251).
