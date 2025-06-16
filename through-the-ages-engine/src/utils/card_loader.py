import csv
import os
import logging
from typing import List, Dict
from game.cards import Card

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
                'resource': row.get('Production Resource', 0),
                'culture': row.get('Production Culture', 0),
                'strength': row.get('Production Strength', 0),
                'happy': row.get('Production Happy', 0),
                'science': row.get('Production Science', 0),
                'civil_action': row.get('Produce civil action', 0),
                'military_action': row.get('Produce military action', 0)
            }

            gain = {
                'food': row.get('Gain Food', 0),
                'resource': row.get('Gain Resource', 0),
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