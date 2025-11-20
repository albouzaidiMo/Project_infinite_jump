# coins.py
import random
import pygame
from os.path import join  
from plateforme import activePlates


class Coin(pygame.sprite.Sprite):
    def __init__(self, image, platform):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()

        self.platform = platform

        # largeur de la plateforme
        width = self.platform.image.get_width()

        # décalage horizontal aléatoire sur la plateforme
        self.offset_x = random.randint(5, max(5, width - 5))

        # position initiale
        self.update_position()

    def update_position(self):
        """Met à jour la position de la pièce en fonction de la plateforme."""
        self.rect.centerx = self.platform.x + self.offset_x
        self.rect.bottom = self.platform.y - 5  # juste au-dessus de la plateforme

    def update(self):
        """Appelé à chaque frame : la pièce suit la plateforme."""
        self.update_position()


class CoinManager:
    """Gère les pièces : création, update, collisions, recyclage."""

    def __init__(self, coin_image, spawn_probability=0.4):
        self.collected = 0
        self.coin_image = coin_image
        self.spawn_probability = spawn_probability
        self.coins = pygame.sprite.Group()

        # --- AJOUT DU SON ---
        try:
            # On charge le son fourni
            self.coin_sound = pygame.mixer.Sound(join("assets", "coin-257878.mp3"))
            self.coin_sound.set_volume(0.2) 
        except Exception as e:
            print(f"Erreur chargement son coin: {e}")
            self.coin_sound = None
        # --------------------

        # Plateformes pour lesquelles on a déjà tenté de créer une pièce
        self.attempted_platforms = set()

        # Dernière position y connue des plateformes
        self.platform_last_y = {}

        # Spawn initial sur les plateformes déjà présentes
        self._initial_spawn()

    # ---------- Spawn / gestion des plateformes ----------

    def _initial_spawn(self):
        """Une première tentative pour toutes les plateformes au début."""
        for p in activePlates:
            self.platform_last_y[p] = p.y
            self.attempted_platforms.add(p)
            self._maybe_spawn_on_platform(p)

    def _has_coin_on(self, platform):
        return any(c.platform is platform for c in self.coins)

    def _maybe_spawn_on_platform(self, platform):
        """Crée éventuellement une pièce sur une plateforme (au max 1 pièce)."""
        if self._has_coin_on(platform):
            return

        if random.random() < self.spawn_probability:
            coin = Coin(self.coin_image, platform)
            self.coins.add(coin)

    def _update_platform_life_cycle(self):
        """
        Détecte quand une plateforme a été recyclée vers le haut.
        """
        THRESHOLD = 50 

        # Nettoyage des plateformes disparues
        for p in list(self.platform_last_y.keys()):
            if p not in activePlates:
                self.platform_last_y.pop(p, None)
                self.attempted_platforms.discard(p)

        # Détection des recyclages
        for p in activePlates:
            old_y = self.platform_last_y.get(p, p.y)
            new_y = p.y

            # Si old_y >> new_y, la plateforme est remontée d'un coup => recyclée
            if old_y - new_y > THRESHOLD:
                self.attempted_platforms.discard(p)

            self.platform_last_y[p] = new_y

    # ---------- Boucle principale du manager ----------

    def update(self):
        """À appeler à chaque frame depuis Jeu.py."""
        # Les pièces suivent leurs plateformes
        for c in self.coins:
            c.update()

        # Retirer les pièces dont la plateforme n'existe plus
        for c in list(self.coins):
            if c.platform not in activePlates:
                self.coins.remove(c)

        # Met à jour le "cycle de vie" des plateformes
        self._update_platform_life_cycle()

        # Pour chaque plateforme sans pièce, si on n'a pas encore tenté dans cette vie -> tenter
        for p in activePlates:
            if (p not in self.attempted_platforms) and (not self._has_coin_on(p)):
                self._maybe_spawn_on_platform(p)
                self.attempted_platforms.add(p)

    # ---------- Affichage & collisions ----------

    def draw(self, screen):
        self.coins.draw(screen)

    def check_collision(self, player_rect, score, amount=10):
        """Si le joueur touche une pièce -> +score et suppression de la pièce."""
        for c in list(self.coins):
            if player_rect.colliderect(c.rect):
                self.collected += 1  
                score.add(amount)  
                self.coins.remove(c)
                
                # --- JOUER LE SON ICI ---
                if self.coin_sound:
                    self.coin_sound.play()
