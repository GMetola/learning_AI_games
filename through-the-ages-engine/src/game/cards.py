# File: /learning_AI_games/through-the-ages-engine/src/game/cards.py
import csv
import os
import logging
from typing import List, Dict


class Card:
    def __init__(self, name, category, age, tech_cost, build_cost, production, gain, card_text, additional_info=None):
        """Inicializa una carta del juego

        Args:
            name (str): Nombre de la carta
            category (str): Categoría (Production, Urban, Military, etc.)
            age (str): Era de la carta (A, I, II, III)
            tech_cost (int): Coste de tecnología
            build_cost (int): Coste de construcción
            production (dict): Recursos que produce la carta
            gain (dict): Recursos que otorga inmediatamente
            card_text (str): Texto descriptivo de la carta
            additional_info (dict): Información adicional (tipo, frecuencia, etc.)
        """
        self.name = name
        self.category = category
        self.age = age
        self.tech_cost = tech_cost
        self.build_cost = build_cost
        self.production = production
        self.gain = gain
        self.card_text = card_text
        self.additional_info = additional_info or {}

    def get_total_production(self) -> int:
        """Calcula la producción total de la carta"""
        return sum(value for value in self.production.values() if isinstance(value, (int, float)))

    def get_total_gain(self) -> int:
        """Calcula la ganancia total inmediata de la carta"""
        return sum(value for value in self.gain.values() if isinstance(value, (int, float)))

    def is_military(self) -> bool:
        """Verifica si la carta es militar"""
        return self.category.lower() == 'military'

    def is_wonder(self) -> bool:
        """Verifica si la carta es una maravilla"""
        return self.category.lower() == 'wonder'

    def get_type(self) -> str:
        """Obtiene el tipo específico de la carta"""
        return self.additional_info.get('type', '')

    def __str__(self):
        return f"Carta: {self.name} ({self.category}, Era {self.age})"

    def __repr__(self):
        return f"Card(name='{self.name}', category='{self.category}', age='{self.age}')"

class CardManager:
    def __init__(self):
        self.cards = []

    def load_cards(self, card_data):
        for data in card_data:
            card = Card(
                name=data['Card Name'],
                category=data['Category'],
                age=data['Age'],
                tech_cost=data['Tech cost'],
                build_cost=data['Build cost'],
                production={
                    'Food': data['Production Food'],
                    'Material': data['Production Material'],
                    'Culture': data['Production Culture'],
                    'Strength': data['Production Strength'],
                    'Happy': data['Production Happy'],
                    'Science': data['Production Science']
                },
                gain={
                    'Food': data['Gain Food'],
                    'Material': data['Gain Material'],
                    'Culture': data['Gain Culture'],
                    'Strength': data['Gain Strength'],
                    'Happy': data['Gain Happy'],
                    'Science': data['Gain Science'],
                    'Civil Action': data['Gain civil action'],
                    'Military Action': data['Gain military action']
                },
                card_text=data['Card text and comments']
            )
            self.cards.append(card)

    def get_card_by_name(self, name):
        for card in self.cards:
            if card.name == name:
                return card
        return None

    def get_all_cards(self):
        return self.cards


class Deck:
    """Clase para gestionar mazos de cartas"""

    def __init__(self, cards: List[Card]):
        """Inicializa el mazo con una lista de cartas

        Args:
            cards (List[Card]): Lista de cartas que componen el mazo
        """
        self.cards = cards

    def shuffle(self):
        """Mezcla las cartas del mazo"""
        import random
        random.shuffle(self.cards)

    def draw(self, count: int) -> List[Card]:
        """Saca un número específico de cartas del mazo

        Args:
            count (int): Número de cartas a sacar

        Returns:
            List[Card]: Lista de cartas sacadas
        """
        return [self.cards.pop() for _ in range(min(count, len(self.cards)))]


class CardLoader:
    def __init__(self, csv_path: str = None):
        """Cargador de cartas desde archivo CSV

        Args:
            csv_path (str): Ruta al archivo CSV con datos de cartas
        """
        if csv_path is None:
            # Ruta por defecto al CSV de cartas
            self.csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'cards.csv')
        else:
            self.csv_path = csv_path

    def load_cards_from_csv(self) -> List[Card]:
        """Carga todas las cartas desde el archivo CSV

        Returns:
            List[Card]: Lista de objetos Card
        """
        cards = []

        try:
            if not os.path.exists(self.csv_path):
                logging.error(f"Archivo CSV no encontrado: {self.csv_path}")
                return []
            with open(self.csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # Convierte valores vacíos a None o 0 según corresponda
                    card_data = self._clean_row_data(row)

                    # Solo incluye cartas marcadas para v0.1
                    included_value = card_data.get('Included v0.1')

                    if included_value == 1 or included_value == '1':  # Acepta tanto int como str
                        card = self._create_card_from_row(card_data)
                        if card:
                            cards.append(card)

            logging.info(f"Cargadas {len(cards)} cartas desde {self.csv_path}")
            return cards

        except FileNotFoundError:
            logging.error(f"Archivo CSV no encontrado: {self.csv_path}")
            return []
        except Exception as e:
            logging.error(f"Error cargando cartas: {e}")
            return []

    def _clean_row_data(self, row: Dict) -> Dict:
        """Limpia y convierte los datos de una fila del CSV"""
        cleaned = {}

        for key, value in row.items():
            if value == '' or value is None:
                # Campos numéricos vacíos se convierten a 0
                if any(field in key for field in ['cost', 'Production', 'Gain', 'Frequency']):
                    cleaned[key] = 0
                else:
                    cleaned[key] = None
            else:
                # Intenta convertir a número si es posible
                try:
                    if '.' in str(value):
                        cleaned[key] = float(value)
                    else:
                        cleaned[key] = int(value)
                except (ValueError, TypeError):
                    cleaned[key] = str(value).strip()

        return cleaned

    def _create_card_from_row(self, row: Dict) -> Card:
        """Crea un objeto Card desde una fila de datos

        Args:
            row (Dict): Datos de la carta desde CSV

        Returns:
            Card: Objeto carta creado
        """
        try:
            # Extrae costes - puede ser un número o una secuencia como "3 4 5"
            tech_cost = self._parse_cost(row.get('Tech cost', 0))
            build_cost = self._parse_cost(row.get('Build cost', 0))

            # Crea diccionarios de producción y ganancia
            production = {
                'food': row.get('Production Food', 0),
                'material': row.get('Production Material', 0),
                'culture': row.get('Production Culture', 0),
                'strength': row.get('Production Strength', 0),
                'happy': row.get('Production Happy', 0),
                'science': row.get('Production Science', 0),
                'civil_action': row.get('Produce civil action', 0),
                'military_action': row.get('Produce military action', 0)
            }

            gain = {
                'food': row.get('Gain Food', 0),
                'material': row.get('Gain Material', 0),
                'culture': row.get('Gain Culture', 0),
                'strength': row.get('Gain Strength', 0),
                'happy': row.get('Gain Happy', 0),
                'science': row.get('Gain Science', 0),
                'civil_action': row.get('Gain civil action', 0),
                'military_action': row.get('Gain military action', 0)
            }

            # Información adicional
            card_info = {
                'type': row.get('Type'),
                'frequency': row.get('Frequency 4 players', 1),
                'blue_token': row.get('Blue token', 0),
                'yellow_token': row.get('Yellow token', 0)
            }

            return Card(
                name=row.get('Card Name'),
                category=row.get('Category'),
                age=row.get('Age'),
                tech_cost=tech_cost,
                build_cost=build_cost,
                production=production,
                gain=gain,
                card_text=row.get('Card text and comments', ''),
                additional_info=card_info
            )

        except Exception as e:
            logging.error(f"Error creando carta desde fila: {e}")
            return None

    def _parse_cost(self, cost_value):
        """Parsea valores de coste que pueden ser números o secuencias"""
        if isinstance(cost_value, (int, float)):
            return cost_value

        if isinstance(cost_value, str):
            # Para costes como "3 4 5" o "2 (7)"
            if '(' in cost_value:
                # Extrae el número entre paréntesis como coste total
                import re
                match = re.search(r'\((\d+)\)', cost_value)
                if match:
                    return int(match.group(1))

            # Para secuencias simples, toma el primer número
            parts = cost_value.split()
            if parts:
                try:
                    return int(parts[0])
                except ValueError:
                    pass

        return 0

# Funciones de compatibilidad con código existente
def load_cards(file_path):
    loader = CardLoader(file_path)
    return loader.load_cards_from_csv()

def get_card_by_name(cards, name):
    for card in cards:
        if hasattr(card, 'name') and card.name == name:
            return card
        elif isinstance(card, dict) and card.get('Card Name') == name:
            return card
    return None

def get_cards_by_category(cards, category):
    result = []
    for card in cards:
        if hasattr(card, 'category') and card.category == category:
            result.append(card)
        elif isinstance(card, dict) and card.get('Category') == category:
            result.append(card)
    return result
