import pyautogui
import time
from Utility.window_detect import getAlbionPos
from Scanner import scan_number_in_region, scan_string_in_region, is_similar
from HelperFuncitons import type_with_delay
from PositionVariables import *


def create_buy_order(item_name, quantity, minimum_difference):
    positions = PositionConfig()
    pyautogui.click(positions.ITEM_NAME_ENTRY_POS)
    time.sleep(0.1)
    pyautogui.write(item_name)
    time.sleep(1)
    pyautogui.click(positions.BUY_BUTTON_POS)
    time.sleep(0.1)

    # Hier wird überprüft, ob die Order-Übersicht bereits geöffnet ist
    order_overview = scan_number_in_region(positions.ORDER_OVERVIEW_REGION)
    print(order_overview)
    if not order_overview:
        pyautogui.moveTo(positions.ORDER_OVERVIEW_TOGGLE_POS)
        time.sleep(6)
        pyautogui.click()
        time.sleep(0.1)
        order_overview = scan_number_in_region(positions.ORDER_OVERVIEW_REGION)
        if not order_overview:
            print("Fehler: Preisübersicht konnte nicht geöffnet werden.")
            return

    # Scanne beste Buy und Sell Order
    sell_price = scan_number_in_region(positions.ORDER_OVERVIEW_REGION)
    buy_price = scan_number_in_region(positions.BEST_BUY_PRICE_REGION)

    print("Detected Prices:", buy_price, sell_price)
    if not sell_price or not buy_price or (sell_price - buy_price) * 100 / sell_price <= minimum_difference:
        print("Fehler: Preisunterschied nicht groß genug.")
        return

    pyautogui.click(positions.BUY_ORDER_POS)
    time.sleep(0.1)
    for _ in range(quantity - 1):
        pyautogui.click(positions.INCREASE_QUANTITY_POS)
        time.sleep(0.1)
    pyautogui.click(positions.INCREASE_PRICE_POS)
    time.sleep(0.1)
    pyautogui.click(positions.CONFIRM_ORDER_POS)
    time.sleep(0.1)
    pyautogui.click(positions.CONFIRM_YES_POS)
    time.sleep(0.1)

    print("Kauforder erfolgreich erstellt.")
    return


def update_buy_order(item_name, quantity, minimum_difference, max_pay_amount):
    positions = PositionConfig()
    # Klick auf "Meine Orders"
    pyautogui.moveTo(positions.MY_ORDERS_POS, duration=0.3)
    pyautogui.click()

    # Klick auf Eingabefeld
    pyautogui.moveTo(positions.ITEM_NAME_ENTRY_POS, duration=0.3)
    pyautogui.click()
    type_with_delay(item_name)

    # Überprüfe ob Order vorhanden
    scanned_name = scan_string_in_region(positions.MY_ORDER_ITEM_NAME)  # Annahme: die Region ist hier korrekt
    print("Scanned name:", scanned_name)
    if scanned_name.strip().lower() != item_name.lower():
        print("Fehler: Order für das Item nicht gefunden.")
        return

    # Anzahl der Items merken
    item_count = scan_number_in_region((positions.EDIT_BUTTON_POS[0] + 300, positions.EDIT_BUTTON_POS[1] - 11, positions.EDIT_BUTTON_POS[0] + 384, positions.EDIT_BUTTON_POS[1] + 19))

    # Aktuellen Order Preis merken
    item_price = scan_number_in_region((positions.EDIT_BUTTON_POS[0] - 158, positions.EDIT_BUTTON_POS[1] - 11, positions.EDIT_BUTTON_POS[0] - 58, positions.EDIT_BUTTON_POS[1] + 19))

    # Klicke auf Bearbeiten
    pyautogui.moveTo(positions.EDIT_BUTTON_POS, duration=0.3)
    pyautogui.click()
    time.sleep(0.2)

    # Überprüfen, ob Preisübersicht geöffnet ist
    order_overview = scan_number_in_region(positions.ORDER_OVERVIEW_REGION)
    if not order_overview:
        pyautogui.moveTo(positions.ORDER_OVERVIEW_TOGGLE_POS, duration=0.3)
        pyautogui.click()
        order_overview = scan_number_in_region(positions.ORDER_OVERVIEW_REGION)
        if not order_overview:
            print("Fehler: Preisübersicht konnte nicht geöffnet werden.")
            return

    # Scanne beste Buy Order
    best_buy_price = scan_number_in_region(positions.BEST_BUY_PRICE_REGION)

    # Setze Preis auf gescannten Preis +1, falls < maxPayAmount
    new_price = best_buy_price + 1
    if item_price == best_buy_price:
        print("Deine Order ist noch die Beste")
    else:
        if new_price < max_pay_amount:
            pyautogui.moveTo(positions.INCREASE_PRICE_POS, duration=0.3)
            pyautogui.click()
            pyautogui.write(str(new_price))
        else:
            print("Fehler: Maximaler Zahlbetrag überschritten.")
            return

    # Klicke (+) bei Anzahl bis gewünschte Anzahl wieder erreicht
    for _ in range(quantity - item_count):
        pyautogui.moveTo(positions.INCREASE_QUANTITY_POS, duration=0.6)
        pyautogui.click()

    # Klicke auf Order Aktualisieren
    pyautogui.moveTo(positions.CONFIRM_ORDER_POS, duration=1)
    pyautogui.click()

    print("Kauforder erfolgreich aktualisiert.")



def collect_items():
    X, Y = getAlbionPos()
    # region in der das "check" symbol sichtbar sein sollte
    screen_region = (X + 1022, Y + 616, X + 1043, Y + 636)
    template_path = 'assets/check.png'
    if is_similar(screen_region, template_path):
        # Bewegen zum Button "Abgeschlossene Handel" und klicken
        pyautogui.moveTo(X + 1040, Y + 615, duration=0.3)
        pyautogui.click()

        time.sleep(0.5)

        # Bewegen zum Button "Alles einsammeln" und klicken
        pyautogui.moveTo(X + 940, Y + 750, duration=0.3)
        pyautogui.click()

        print("Items erfolgreich eingesammelt.")
    else:
        print("Keine Abholbereiten items erkannt")
