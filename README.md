# Talking Dashboard — Tableau de bord vocal de supervision

Projet Open Innovation EPSI / WIS — 2025 / 2026  

---

## Présentation

Le **Talking Dashboard** est une solution de supervision informatique qui annonce vocalement les incidents détectés dans l'infrastructure. Quand un serveur tombe, le système le détecte en moins de 15 secondes, affiche une alerte sur le dashboard et annonce vocalement l'incident via les haut-parleurs. Quand le serveur revient en ligne, la voix annonce également la résolution.

Aucun outil du marché (Grafana, Zabbix, Nagios, Centreon) ne propose cette fonctionnalité nativement. C'est l'innovation principale du projet.

---

## Architecture

```
server-1 (Node Exporter :9101)  ─┐
server-2 (Node Exporter :9102)  ─┼──► Prometheus :9090 ──► Alertmanager :9093
server-3 (Node Exporter :9103)  ─┘                                │
                                                                   │ Webhook
                                                          App Vocale Python :5000
                                                          (Flask + pyttsx3)
                                                                   │
                                                          Dashboard Web :8080
                                                          (HTML / CSS / JS)
```

---

## Technologies utilisées

| Technologie | Rôle |
|---|---|
| Prometheus | Collecte des métriques toutes les 10 secondes |
| Node Exporter | Expose les métriques CPU, RAM, Disque, Réseau |
| Alertmanager | Gère et route les alertes via Webhook |
| Python Flask | Reçoit les alertes et déclenche la synthèse vocale |
| pyttsx3 | Synthèse vocale sur Windows |
| HTML / CSS / JS | Dashboard web temps réel |
| Docker Compose | Orchestration de toute l'infrastructure |

---

## Prérequis

- Windows 10 / 11
- Docker Desktop installé et démarré
- Python 3.11+
- Git

---

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/nina296/talking-dashboard.git
cd talking-dashboard
```

### 2. Installer les dépendances Python

```bash
cd vocal-app
pip install flask flask-cors pyttsx3 requests
cd ..
```

---

## Lancement

### Terminal 1 — Infrastructure Docker

```bash
docker compose up
```

### Terminal 2 — Application vocale Windows

```bash
cd vocal-app
python app.py
```

### Accès aux interfaces

| Interface | URL |
|---|---|
| Dashboard Web | http://localhost:8080 |
| Prometheus | http://localhost:9090 |
| Alertmanager | http://localhost:9093 |
| App Vocale | http://localhost:5000 |

---

## Structure du projet

```
talking-dashboard/
├── docker-compose.yml
├── prometheus/
│   ├── prometheus.yml        # Configuration Prometheus
│   └── alerts.yml            # Règles d'alerte
├── alertmanager/
│   └── alertmanager.yml      # Configuration Alertmanager
├── vocal-app/
│   ├── app.py                # Application Flask + synthèse vocale
│   ├── requirements.txt      # Dépendances Python
│   └── Dockerfile
├── dashboard/
│   ├── index.html            # Dashboard web complet
│   └── Dockerfile
└── README.md
```

---

## Fonctionnalités

- Surveillance de 3 serveurs simulés (server-1, server-2, server-3)
- Métriques affichées en temps réel : CPU, RAM, Disque, Réseau RX/TX
- Détection automatique d'un serveur hors ligne en moins de 15 secondes
- Alerte vocale automatique quand un serveur tombe
- Alerte vocale de résolution quand un serveur revient en ligne
- Historique des alertes sur le dashboard
- Bouton de test vocal
- État global du système (OK / Warning / Incident)

---

## Seuils d'alerte

| Métrique | Seuil Warning | Seuil Critical |
|---|---|---|
| CPU | — | > 80% pendant 30s |
| RAM | — | > 80% pendant 30s |
| Disque | > 85% pendant 1min | — |
| Disponibilité serveur | — | 0 (hors ligne) pendant 10s |

---

## Test de la solution

### Simuler une panne

```bash
# Éteindre un serveur
docker stop server-2

# Attendre 15 secondes
# → Le dashboard affiche server-2 en rouge
# → La voix annonce "Attention ! Server-2 est hors ligne..."
```

### Simuler une résolution

```bash
# Rallumer le serveur
docker start server-2

# Attendre 15 secondes
# → Le dashboard repasse au vert
# → La voix annonce "Bonne nouvelle. Server-2 est de nouveau en ligne..."
```

### Tester la voix manuellement

```bash
curl http://localhost:5000/test
```

---

## Arrêt du projet

```bash
# Arrêter Docker
docker compose down

# Arrêter l'app vocale
# Ctrl+C dans le terminal Python
```

