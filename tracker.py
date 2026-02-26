import json
import os
from datetime import datetime

# Commit (EN):
# Implement CLI order tracking tool
#
# - Store freelance orders in orders.json
# - Add interactive menu for managing orders
# - Support adding, listing and editing orders
# - Calculate total income and completed income
# - Mark orders as completed and reset all data
#
# Коммит (RU):
# Реализовать консольный трекер заказов
#
# - Хранить заказы фриланса в orders.json
# - Добавить интерактивное меню для управления заказами
# - Поддержать добавление, просмотр и редактирование заказов
# - Считать общий доход и доход по выполненным заказам
# - Отмечать заказы выполненными и полностью очищать данные

FILENAME = "orders.json"

def load_orders():
    if not os.path.exists(FILENAME):
        return []  # если файла нет — возвращаем пустой список

    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []

def save_orders(orders):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

def next_order_id(orders):
    if not orders:
        return 1
    return max(int(o.get("id", 0)) for o in orders) + 1

def normalize_status(value, default=None):
    if value is None:
        return default
    s = str(value).strip().lower()
    if s == "":
        return default

    if s in {"+", "выполнен", "выполнено", "готово", "done"}:
        return "выполнен"
    if s in {"-", "в работе", "работа", "вработе", "work", "in work", "inwork"}:
        return "в работе"

    return None

def input_status(prompt, default=None, allow_empty=False):
    hint = "в работе / выполнен (можно '-' или '+')"
    while True:
        raw = input(f"{prompt} [{hint}]: ").strip()
        if raw == "" and allow_empty:
            return None
        normalized = normalize_status(raw, default=default)
        if normalized is not None:
            return normalized
        print("Статус не распознан. Введи 'в работе' или 'выполнен' (или '-' / '+').")

def add_order(client, amount, status="в работе"):
    orders = load_orders()
    order = {
        "id": next_order_id(orders),
        "client": client,
        "amount": amount,
        "status": normalize_status(status, default="в работе") or "в работе",
        "date": datetime.now().strftime("%d.%m.%Y")
    }
    orders.append(order)
    save_orders(orders)
    print(f"Заказ добавлен: {client} — ${amount}")

def show_orders():
    orders = load_orders()
    if not orders:
        print("Заказов пока нет")
        return
    print("\n=== Все заказы ===")
    for order in orders:
        print(f"#{order['id']} | {order['date']} | {order['client']} | ${order['amount']} | {order['status']}")

def show_income():
    orders = load_orders()
    total = sum(order['amount'] for order in orders)
    completed = sum(order['amount'] for order in orders if order['status'] == "выполнен")
    print(f"\nОбщий доход: ${total}")
    print(f"Получено (выполнено): ${completed}")
    print(f"В работе: ${total - completed}")

def find_order_index_by_id(orders, order_id):
    for i, order in enumerate(orders):
        if int(order.get("id", -1)) == order_id:
            return i
    return None

def input_int(prompt, allow_empty=False):
    while True:
        raw = input(prompt).strip()
        if raw == "" and allow_empty:
            return None
        try:
            return int(raw)
        except ValueError:
            print("Нужно число. Попробуй снова.")

def edit_order():
    orders = load_orders()
    if not orders:
        print("Заказов пока нет")
        return

    show_orders()
    order_id = input_int("\nВведите ID заказа для редактирования: ")
    idx = find_order_index_by_id(orders, order_id)
    if idx is None:
        print("Заказ с таким ID не найден.")
        return

    order = orders[idx]
    print("\nEnter = оставить как есть.")
    new_client = input(f"Клиент [{order.get('client', '')}]: ").strip()
    if new_client != "":
        order["client"] = new_client

    new_amount = input_int(f"Сумма ($) [{order.get('amount', '')}]: ", allow_empty=True)
    if new_amount is not None:
        order["amount"] = new_amount

    new_status = input_status(f"Статус [{order.get('status', '')}]", allow_empty=True)
    if new_status is not None:
        order["status"] = new_status

    save_orders(orders)
    print("Заказ обновлён.")

def mark_order_completed():
    orders = load_orders()
    if not orders:
        print("Заказов пока нет")
        return

    show_orders()
    order_id = input_int("\nВведите ID заказа, чтобы отметить выполненным: ")
    idx = find_order_index_by_id(orders, order_id)
    if idx is None:
        print("Заказ с таким ID не найден.")
        return

    if orders[idx].get("status") == "выполнен":
        print("Этот заказ уже выполнен.")
        return

    orders[idx]["status"] = "выполнен"
    save_orders(orders)
    print("Статус изменён на 'выполнен'.")

def reset_all_data():
    confirm = input("Точно сбросить ВСЕ заказы? Введи ДА для подтверждения: ").strip().lower()
    if confirm not in {"да", "da", "yes", "y"}:
        print("Сброс отменён.")
        return
    save_orders([])
    print("Всё очищено. База заказов пустая.")

def main():
    while True:
        print("\n=== Трекер заказов ===")
        print("1. Добавить заказ")
        print("2. Показать все заказы")
        print("3. Показать доход")
        print("4. Изменить данные заказа")
        print("5. Отметить заказ выполненным")
        print("6. Сбросить всю статистику")
        print("7. Выход")

        choice = input("\nВыбери пункт: ")

        if choice == "1":
            client = input("Имя клиента: ")
            amount = input_int("Сумма ($): ")
            status = input_status("Статус", default="в работе")
            add_order(client, amount, status)
        elif choice == "2":
            show_orders()
        elif choice == "3":
            show_income()
        elif choice == "4":
            edit_order()
        elif choice == "5":
            mark_order_completed()
        elif choice == "6":
            reset_all_data()
        elif choice == "7":
            print("Выход...")
            break
        else:
            print("Неверный пункт, попробуй снова")

if __name__ == "__main__":
    main()