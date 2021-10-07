from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from datetime import datetime
import sqlite3
import os
import sys
import requests

# Global variable to update the active trades if necessary
UPDATED = 0


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for production"""
    base_path = getattr(sys, 'MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class TabPanel(TabbedPanel):
    # Initial value for date.
    date = datetime.today().strftime("%d/%m/%Y")

    def update_grid(self):
        global UPDATED
        if UPDATED > 0:
            item = self.ids["Active_Trades"]
            item.clear_widgets()
            grid = Trades.build_grid(self)
            item.add_widget(grid)

    def data_validation(self):
        # Validate that all the information has been captured correctly.

        # Date
        try:
            date = datetime.strptime(self.ids.Date.text, '%d/%m/%Y')
            date = date.strftime("%d/%m/%Y")
        except:
            title = "Invalid Date"
            error_message = "You have typed an invalid date.\nPlease retype according to the hint: dd/mm/yyyy"
            Trades.message(title, error_message)
            return

        # Symbol
        symbol = self.ids.Symbol.text
        if len(symbol) == 0:
            title = "Empty Symbol"
            error_message = "You can not leave the symbol empty"
            Trades.message(title, error_message)
            return

        if symbol.find("/") == -1:
            title = "Invalid Symbol"
            error_message = "You have typed an invalid symbol.\nPlease retype according to the hint: BTC/USDT"
            Trades.message(title, error_message)
            return
        symbol = symbol.upper()

        # Direction
        if self.ids.Long.state == "normal" and self.ids.Short.state == "normal":
            title = "Missing Direction"
            error_message = "You must select a direction for the trade"
            Trades.message(title, error_message)
            return

        if self.ids.Long.state == "down":
            direction = "Long"

        if self.ids.Short.state == "down":
            direction = "Short"

        # Entry Price
        try:
            entry_price = float(self.ids.Entry_Price.text)

            if entry_price <= 0:
                title = "Entry Price Value"
                error_message = "Entry Price value has to be greater than 0"
                Trades.message(title, error_message)
                return
        except:
            title = "Entry Price Value"
            error_message = "Entry Price value has to be a number"
            Trades.message(title, error_message)
            return

        # Exit 1
        try:
            exit1 = float(self.ids.Exit1.text)

            if exit1 <= 0:
                title = "Exit 1 Value"
                error_message = "Exit 1 value has to be greater than 0"
                Trades.message(title, error_message)
                return
        except:
            title = "Exit 1 Value"
            error_message = "Exit 1 value has to be a number"
            Trades.message(title, error_message)
            return

        # Exit 2
        try:
            exit2 = float(self.ids.Exit2.text)
        except:
            exit2 = 0

        # Exit 3
        try:
            exit3 = float(self.ids.Exit3.text)
        except:
            exit3 = 0

        # Exit 4
        try:
            exit4 = float(self.ids.Exit4.text)
        except:
            exit4 = 0

        # Stop Loss
        try:
            stop_loss = float(self.ids.Stop_Loss.text)

            if stop_loss <= 0:
                title = "Stop Loss Value"
                error_message = "Stop Loss value has to be greater than 0"
                Trades.message(title, error_message)
                return
        except:
            title = "Stop Loss Value"
            error_message = "Stop Loss value has to be a number"
            Trades.message(title, error_message)
            return

        current_price = 0
        active_id = 1

        # Returns every textbox to initial values.
        self.ids.Date.text = ""
        self.ids.Symbol.text = ""
        self.ids.Long.state = "normal"
        self.ids.Short.state = "normal"
        self.ids.Entry_Price.text = ""
        self.ids.Exit1.text = ""
        self.ids.Exit2.text = ""
        self.ids.Exit3.text = ""
        self.ids.Exit4.text = ""
        self.ids.Stop_Loss.text = ""

        query = '''INSERT INTO active_trades(date, symbol, direction, entry_price, current_price, exit1, exit2, 
        exit3, exit4, stop_loss, active_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
        data = (date, symbol, direction, entry_price, current_price, exit1, exit2, exit3, exit4, stop_loss, active_id)

        Trades.sql(self, "trades.db", query, data, 2)
        global UPDATED
        UPDATED += 1


class Trades(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_resize=self.on_window_resize)

    def build(self):

        # Creates the static objects
        tab = TabPanel()

        # Creates and adds the dynamic objects
        tab.ids.Active_Trades.add_widget(self.build_grid())

        return tab

    def build_grid(self):

        # Query for the information.
        query = "SELECT a.* FROM active_trades a WHERE a.active_id = 1"
        result = Trades.sql(self, "trades.db", query, "", 1)

        # Establish Grid properties
        grid = GridLayout()
        grid.cols = 10
        grid.rows = len(result) + 2
        grid.orientation = "lr-tb"
        grid.spacing = 10
        grid.padding = 10

        # Grid header
        grid.add_widget(Label(text="Date", bold=True))
        grid.add_widget(Label(text="Symbol", bold=True))
        grid.add_widget(Label(text="Direction", bold=True))
        grid.add_widget(Label(text="Entry Price", bold=True))
        grid.add_widget(Label(text="Current Price", bold=True))
        grid.add_widget(Label(text="Exit 1", bold=True))
        grid.add_widget(Label(text="Exit 2", bold=True))
        grid.add_widget(Label(text="Exit 3", bold=True))
        grid.add_widget(Label(text="Exit 4", bold=True))
        grid.add_widget(Label(text="Stop Loss", bold=True))

        # Add the info into the grid
        for i, row in enumerate(result):
            for j in range(1, 11):

                item = TextInput(text=str(result[i][j]), readonly="True",
                                 halign="center", foreground_color=(1, 1, 1, 1))

                # Cells that will have a conditional background color
                item.background_color = Trades.colors(self, result[i], j)
                item.font_size = (item.width + item.height) / 21
                grid.add_widget(item)

        for i in range(9):
            grid.add_widget(Label(text=""))

        grid.add_widget(Button(text="Update", on_release=Trades.get_price))
        scroll = ScrollView()
        scroll.add_widget(grid)

        return scroll

    def colors(self, result, j):
        # Function that establishes the color of each box.

        # Colors
        yellow = (255 / 255, 225 / 255, 126 / 255, 1)
        green = (128 / 255, 255 / 255, 120 / 255, 1)
        default = (0.2, 0.2, 0.2, 1)

        # Cells with conditional colors
        if j == 4 or j == 6 or j == 7 or j == 8 or j == 9:
            try:
                percentage = (result[5] / result[j]) * 100
            except:
                return default

            if 90 <= percentage < 98:
                return yellow

            if percentage > 98:
                return green

            if percentage < 90:
                return default

        return default

    def message(title, error_message):
        # Dynamic MessageBox
        content = GridLayout()
        content.rows = 2

        pop = Popup(title=title, content=content)
        pop.size_hint = 0.5, 0.5
        pop.auto_dismiss = False
        pop.title_size = Window.width / 50
        content.add_widget(Label(text=error_message, bold=True, font_size=Window.width / 50))
        content.add_widget(Button(text="Accept", bold=True, on_press=pop.dismiss, font_size=Window.width / 20))

        pop.open()

    def sql(self, db, query, data, query_type):
        # Establish connection with the database.
        con = sqlite3.connect(resource_path(db))

        # Creates the cursor for the query.
        cur = con.cursor()

        # Try to run the query
        try:
            # Select query
            if query_type == 1:

                result = cur.execute(query)
                data_list = []

                for row in result:
                    data_list.append(row)

            # Insert/Update query
            if query_type == 2:
                cur.execute(query, data)

        # The query failed and the connection with the db is finished
        except:
            con.commit()
            cur.close()
            title = "Error With The Database"
            error_message = "A problem has occurred while the transaction with the database"
            Trades.message(title, error_message)
            return

        # The query was successful and the connection with the database is finished.
        finally:
            con.commit()
            cur.close()

            if query_type == 1:
                return data_list

            if query_type == 2:
                return

    def on_window_resize(self, window, width, height):

        for i, child in enumerate(self.root.children[0].children[0].children[0].children):
            item = self.root.children[0].children[0].children[0].children[i]
            item.font_size = (width + height) / 145
            try:
                item.padding = (0, item.font_size / 1.3, 0, 0)
            except:
                continue

    def get_price(self, *args):

        main = Trades.get_running_app()

        # Count the total of children inside the object
        object_count = len(main.root.children[0].children[0].children[0].children)
        symbols = []
        prices = []
        sql_symbols = []

        # Loop through the children
        for i, child in enumerate(main.root.children[0].children[0].children[0].children):

            item = main.root.children[0].children[0].children[0].children[i]

            # Skips the label Symbol
            if isinstance(item, Label):
                continue

            # If the number of children matches with the position searched, save the symbol
            if i in range(18, object_count, 10):
                sql_symbols.append(item.text)
                item = "symbol=" + item.text.replace("/", "")
                symbols.append(item)

        # Ask Binance web what is the current price of each token
        for symbol in symbols:
            response = requests.get("http://binance.com/api/v3/ticker/price", params=symbol)

            # Check each response in case something is wrong.
            if response.status_code == 400:
                title = "Invalid Symbol"
                error_message = "You have submitted an invalid symbol\n" + symbol
                self.message(title, error_message)
                return

            if response.status_code == 403:
                title = "Firewall Violation"
                error_message = "The webpage firewall has benn violated"
                self.message(title, error_message)
                return

            if response.status_code == 429:
                title = "Exceeded Queries"
                error_message = "You have exceeded the maximum number of queries "
                self.message(title, error_message)
                return

            if response.status_code == 418:
                title = "Blocked IP"
                error_message = "You IP has been blocked"
                self.message(title, error_message)
                return

            if response.status_code == 500:
                title = "Binance Problem"
                error_message = "Binance has internal problems"
                self.message(title, error_message)
                return

            if response.status_code == 200:
                prices.append(response.json()["price"])

        # Update the database with the updated info
        query = """UPDATE active_trades SET current_price = ? WHERE symbol = ? """
        for i, price in enumerate(prices):
            data = (float(price), sql_symbols[i])
            Trades.sql(self, "trades.db", query, data, 2)

        Trades.update(self, prices)

    def update(self, prices):

        main = Trades.get_running_app()

        yellow = (255 / 255, 225 / 255, 126 / 255, 1)
        green = (128 / 255, 255 / 255, 120 / 255, 1)
        default = (0.2, 0.2, 0.2, 1)

        # Count the objects in the widget
        j = 0
        object_count = len(main.root.children[0].children[0].children[0].children)

        # Loop through each widget finding the ones of current price
        for i, child in enumerate(main.root.children[0].children[0].children[0].children):

            item = main.root.children[0].children[0].children[0].children[i]

            # Skips the label Symbol
            if isinstance(item, Label):
                continue

            # If the widget matches, replace the previous price with the updated price.
            if i in range(15, object_count, 10):
                item.text = str(round(float(prices[j]), 6))
                j += 1

        for j in range(11, 17, 1):

            if j == 15:
                continue

            for i, child in enumerate(main.root.children[0].children[0].children[0].children):

                k = 15 - j

                # Update entry price cell
                if i in range(j, object_count, 10):
                    item = main.root.children[0].children[0].children[0].children[i]

                    if isinstance(item, Label):
                        continue

                    item_value = float(item.text)

                    if item_value == 0:
                        continue

                    current_price = float(main.root.children[0].children[0].children[0].children[i + k].text)

                    percentage = (current_price / item_value) * 100

                    if 90 <= percentage < 98:
                        item.background_color = yellow

                    if percentage > 98:
                        item.background_color = green

                    if percentage < 90:
                        item.background_color = default


if __name__ == "__main__":
    Trades().run()
