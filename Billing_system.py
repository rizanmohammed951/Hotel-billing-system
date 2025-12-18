import wx
import csv


food_menu = {}   

data = csv.reader(open("file1.csv", "r"))
next(data)

for row in data:
    roll = row[0]
    item = row[1]
    price = float(row[2])
    food_menu[roll] = (item, price)


rooms = {
    "Single Room": 1500,
    "Double Room": 2500,
    "Deluxe Room": 4000,
    "Suite": 6000
}


class HotelApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Hotel Billing System", size=(1080, 720))
        panel = wx.Panel(self)

        # Title
        title = wx.StaticText(panel, label="Hotel Billing System")
        title.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        # Inputs
        self.name_box = wx.TextCtrl(panel)
        self.room_box = wx.ComboBox(panel, choices=list(rooms.keys()), style=wx.CB_READONLY)
        self.night_box = wx.TextCtrl(panel)
        self.addon_box = wx.ComboBox(
            panel,
            choices=["None", "Breakfast ₹200", "Laundry ₹300", "Both ₹500"],
            style=wx.CB_READONLY
        )

        # MULTIPLE FOOD SELECTION
        self.food_box = wx.CheckListBox(panel, choices=list(food_menu.keys()))

        # Food menu display
        food_area = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(200, 100))
        for k, (item, price) in food_menu.items():
            food_area.AppendText(f"{k}. {item} - ₹{price}\n")

        # Bill area
        self.bill_area = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(450, 250))

        # Button
        btn = wx.Button(panel, label="Generate Bill")
        btn.Bind(wx.EVT_BUTTON, self.make_bill)

        # Layout
        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(title, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        s.Add(wx.StaticText(panel, label="Customer Name:"))
        s.Add(self.name_box, 0, wx.EXPAND | wx.ALL, 5)

        s.Add(wx.StaticText(panel, label="Room Type:"))
        s.Add(self.room_box, 0, wx.EXPAND | wx.ALL, 5)

        s.Add(wx.StaticText(panel, label="Number of Nights:"))
        s.Add(self.night_box, 0, wx.EXPAND | wx.ALL, 5)

        s.Add(wx.StaticText(panel, label="Add-on Service:"))
        s.Add(self.addon_box, 0, wx.EXPAND | wx.ALL, 5)

        s.Add(wx.StaticText(panel, label="Food Items (Select multiple):"))
        s.Add(self.food_box, 0, wx.EXPAND | wx.ALL, 5)

        s.Add(wx.StaticText(panel, label="Food Menu:"))
        s.Add(food_area, 0, wx.ALL, 5)

        s.Add(btn, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        s.Add(wx.StaticText(panel, label="Bill Output:"))
        s.Add(self.bill_area, 0, wx.ALL, 5)

        panel.SetSizer(s)
        self.Show()

    def make_bill(self, event):
        name = self.name_box.GetValue()
        room = self.room_box.GetValue()
        nights = self.night_box.GetValue()
        addon = self.addon_box.GetValue()

        # BASIC CHECKS
        if name == "" or room == "" or nights == "":
            self.bill_area.SetValue("Please fill all required fields.")
            return

        if not nights.isdigit():
            self.bill_area.SetValue("Nights must be a number.")
            return

        nights = int(nights)

        # Room charge
        room_cost = rooms[room] * nights
        total = room_cost

        # Add-on charges
        if addon.startswith("Breakfast"):
            total += 200 * nights
        elif addon.startswith("Laundry"):
            total += 300
        elif addon.startswith("Both"):
            total += 500 * nights

        # Food charges (multiple)
        food_total = 0
        food_list = []

        checked = self.food_box.GetCheckedItems()
        for index in checked:
            roll = self.food_box.GetString(index)
            item, price = food_menu[roll]
            food_total += price
            food_list.append(f"{item} (₹{price})")

        total += food_total

        # GST
        gst = total * 0.12
        final = total + gst

        # Print Bill
        self.bill_area.SetValue("")
        self.bill_area.AppendText("========= YOUR BILL =========\n")
        self.bill_area.AppendText(f"Name: {name}\n")
        self.bill_area.AppendText(f"Room: {room}\n")
        self.bill_area.AppendText(f"Nights: {nights}\n")
        self.bill_area.AppendText(f"Add-on: {addon}\n\n")

        if food_list:
            self.bill_area.AppendText("Food Items:\n")
            for f in food_list:
                self.bill_area.AppendText(f"  - {f}\n")
        else:
            self.bill_area.AppendText("Food Items: None\n")

        self.bill_area.AppendText(f"\nRoom Charge: ₹{room_cost}\n")
        self.bill_area.AppendText(f"Food Total: ₹{food_total}\n")
        self.bill_area.AppendText(f"Total Before GST: ₹{total:.2f}\n")
        self.bill_area.AppendText(f"GST (12%): ₹{gst:.2f}\n")
        self.bill_area.AppendText(f"GRAND TOTAL: ₹{final:.2f}\n")
        self.bill_area.AppendText("=============================\n")
        self.bill_area.AppendText("Thank you! Visit Again 😊")


app = wx.App()
HotelApp()
app.MainLoop()