import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --- Data for the Application ---
# We store all the text and checklist items in a dictionary
# for easy access.
APP_DATA = {
    "Marriage": {
        "checklist": [
            "Set a budget (venue, food, attire, etc.)",
            "Discuss financial goals and habits with partner",
            "Create a joint bank account (or plan for managing shared expenses)",
            "Review and update beneficiaries on all accounts",
            "Update wills and estate plans",
            "Review health insurance options (joint vs. separate)",
            "Create a plan for managing/paying off any individual debts"
        ],
        "financial_tips": "The average cost of a wedding can be substantial. Start a dedicated high-yield savings account early. More importantly, marriage involves merging two financial lives. Open communication about debt, savings goals, and credit scores is critical for a healthy financial future together.",
        "products": (
            "• Joint Checking/Savings Accounts\n"
            "• High-Yield Savings Account (for wedding fund)\n"
            "• Life Insurance (especially if one partner is financially dependent)\n"
            "• Updated Renter's/Homeowner's Insurance (joint policy)\n"
            "• Credit Cards (consider a joint card for shared expenses)"
        ),
        "advisor_info": "A financial advisor can be invaluable in helping you and your partner merge your finances. They can help you create a joint budget, set long-term goals (like buying a house), and develop a strategy for tackling debt and investing as a team."
    },
    "Having a Child": {
        "checklist": [
            "Estimate hospital and delivery costs (check insurance coverage)",
            "Research and budget for childcare (daycare, nanny, etc.)",
            "Create/update your will to name a guardian",
            "Update life insurance policies (increase coverage)",
            "Review health insurance and add the child to your plan",
            "Start a 529 College Savings Plan",
            "Budget for ongoing costs (diapers, formula, clothes, etc.)"
        ],
        "financial_tips": "The cost of raising a child to age 18 is significant. The biggest new expenses are often childcare and healthcare. Start saving for college as early as possible, even small, regular contributions to a 529 plan can make a big difference over time.",
        "products": (
            "• Life Insurance (Term Life is often recommended for new parents)\n"
            "• Disability Insurance (to protect your income)\n"
            "• 529 College Savings Plan\n"
            "• Health Savings Account (HSA) (if you have a high-deductible plan)\n"
            "• High-Yield Savings Account (for an emergency fund)"
        ),
        "advisor_info": "Balancing your own retirement savings with saving for a child's education is a major financial challenge. An advisor can help you prioritize and create a plan that addresses both long-term goals without sacrificing your own financial security."
    },
    "Buying a House": {
        "checklist": [
            "Check your credit score and report",
            "Determine how much house you can afford (use a 28/36 rule)",
            "Save for a down payment (20% is ideal to avoid PMI)",
            "Save for closing costs (typically 2-5% of home price)",
            "Get pre-approved for a mortgage from multiple lenders",
            "Create a budget for new expenses (property tax, insurance, utilities, maintenance)",
            "Build an emergency fund for unexpected home repairs"
        ],
        "financial_tips": "Your mortgage payment (PITI: Principal, Interest, Taxes, Insurance) is only part of the cost. Budget an additional 1-3% of the home's value per year for maintenance and repairs. A 20% down payment helps you avoid Private Mortgage Insurance (PMI), which saves you money.",
        "products": (
            "• Mortgage (Fixed-Rate or Adjustable-Rate)\n"
            "• Homeowner's Insurance (required by lenders)\n"
            "• Private Mortgage Insurance (PMI) (if down payment < 20%)\n"
            "• Life Insurance (to cover the mortgage for your family)\n"
            "• Flood/Earthquake Insurance (if in a high-risk area)"
        ),
        "advisor_info": "A financial advisor and a mortgage broker are key partners. The broker finds the right loan for you, while the advisor helps you understand how this major purchase fits into your overall financial picture, including its impact on your investments and retirement."
    },
    "Retirement": {
        "checklist": [
            "Calculate your 'retirement number' (estimated savings needed)",
            "Maximize contributions to 401(k), IRAs, or other retirement accounts",
            "Review your investment asset allocation (e.g., stocks vs. bonds)",
            "Create a plan for paying off all debt (especially mortgage)",
            "Estimate your future expenses in retirement",
            "Research Social Security benefit options and claiming strategies",
            "Create/update your estate plan (will, trusts, power of attorney)"
        ],
        "financial_tips": "The most powerful tool you have is time. Start saving as early as possible to take advantage of compound growth. As you get closer to retirement, your focus may shift from aggressive growth to capital preservation. Don't forget to budget for healthcare, as it's often one of the largest expenses in retirement.",
        "products": (
            "• 401(k) or 403(b) (employer-sponsored plan)\n"
            "• Traditional or Roth IRA (individual accounts)\n"
            "• Health Savings Account (HSA) (can be used for health costs in retirement)\n"
            "• Annuities (for guaranteed income, consult an advisor)\n"
            "• Long-Term Care Insurance"
        ),
        "advisor_info": "Retirement planning is complex, with "
    }
}


class LifeEventPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Life Event Planner")
        self.root.geometry("800x600")

        # Set a modern theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TNotebook.Tab', padding=[10, 5], font=('Arial', 10, 'bold'))
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10, 'bold'))
        self.style.configure('TLabelframe.Label', font=('Arial', 11, 'bold'))

        # --- Top Selection Frame ---
        selection_frame = ttk.Frame(self.root, padding=10)
        selection_frame.pack(fill='x')

        ttk.Label(selection_frame, text="Select a Major Life Event:", font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=5)

        self.event_options = list(APP_DATA.keys())
        self.current_event = tk.StringVar(self.root)
        self.current_event.set(self.event_options[0])  # Set default

        event_menu = ttk.OptionMenu(selection_frame, self.current_event, self.event_options[0], *self.event_options)
        event_menu.pack(side=tk.LEFT, padx=5, fill='x', expand=True)

        load_button = ttk.Button(selection_frame, text="Load Plan", command=self.load_event_plan)
        load_button.pack(side=tk.LEFT, padx=5)

        # --- Main Content Frame ---
        # This frame will hold the Notebook (tabs)
        self.content_frame = ttk.Frame(self.root, padding=10)
        self.content_frame.pack(fill='both', expand=True)

        # Load the default event on startup
        self.load_event_plan()

    def clear_frame(self, frame):
        """Helper function to destroy all widgets in a frame."""
        for widget in frame.winfo_children():
            widget.destroy()

    def load_event_plan(self):
        """Clears the content_frame and loads the tabs for the selected event."""
        self.clear_frame(self.content_frame)

        event_name = self.current_event.get()
        event_data = APP_DATA.get(event_name)

        if not event_data:
            messagebox.showerror("Error", "Could not find data for the selected event.")
            return

        # Create the Notebook (tabbed interface)
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill='both', expand=True)

        # Create the four tabs
        tab1 = self.create_checklist_tab(notebook, event_data['checklist'])
        tab2 = self.create_financial_tab(notebook, event_data['financial_tips'])
        tab3 = self.create_products_tab(notebook, event_data['products'])
        tab4 = self.create_advisor_tab(notebook, event_data['advisor_info'])

        # Add tabs to the notebook
        notebook.add(tab1, text="Checklist")
        notebook.add(tab2, text="Financial Impact")
        notebook.add(tab3, text="Recommended Products")
        notebook.add(tab4, text="Find an Advisor")

    def create_checklist_tab(self, parent, checklist_items):
        """Creates the Checklist tab with a scrollable list of checkbuttons."""
        # This is a bit complex, but it creates a scrollable frame
        outer_frame = ttk.Frame(parent, padding=10)
        
        canvas = tk.Canvas(outer_frame, borderwidth=0, background="#ffffff")
        scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding=5)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add checklist items
        for item in checklist_items:
            var = tk.IntVar()
            # Create a frame for each checkbutton + label to keep them together
            item_frame = ttk.Frame(scrollable_frame)

            cb = ttk.Checkbutton(item_frame, variable=var)
            cb.pack(side='left', anchor='nw', padx=5)

            label = ttk.Label(item_frame, text=item, wraplength=600)
            label.pack(side='left', anchor='w', fill='x', expand=True)

            item_frame.pack(anchor='w', fill='x', pady=2) # Add a little vertical padding

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return outer_frame

    def create_financial_tab(self, parent, financial_tips):
        """Creates the Financial Impact tab with the simple simulator."""
        frame = ttk.Frame(parent, padding=10)

        # --- Simulator Frame ---
        sim_frame = ttk.LabelFrame(frame, text="Simple Financial Simulator", padding=10)
        sim_frame.pack(fill='x', pady=10)

        # Cost Entry
        ttk.Label(sim_frame, text="Estimated Cost of Event:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.cost_entry = ttk.Entry(sim_frame, width=20)
        self.cost_entry.grid(row=0, column=1, sticky='w', padx=5, pady=5)

        # Savings Entry
        ttk.Label(sim_frame, text="Current Savings for Event:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.savings_entry = ttk.Entry(sim_frame, width=20)
        self.savings_entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        # Calculate Button
        calc_button = ttk.Button(sim_frame, text="Calculate Gap", command=self.calculate_gap)
        calc_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Result Label
        self.gap_result_label = ttk.Label(sim_frame, text="Savings Gap: $0.00", font=('Arial', 12, 'bold'))
        self.gap_result_label.grid(row=3, column=0, columnspan=2, pady=5)
        
        # --- Tips Frame ---
        tips_frame = ttk.LabelFrame(frame, text="Key Financial Considerations", padding=10)
        tips_frame.pack(fill='both', expand=True, pady=10)
        
        tips_label = ttk.Label(tips_frame, text=financial_tips, wraplength=700, justify='left')
        tips_label.pack(anchor='w')
        
        return frame

    def calculate_gap(self):
        """Callback for the 'Calculate Gap' button."""
        try:
            cost = float(self.cost_entry.get() or 0)
            savings = float(self.savings_entry.get() or 0)
            
            gap = cost - savings
            
            if gap > 0:
                self.gap_result_label.config(text=f"Savings Gap: ${gap:,.2f}", foreground='red')
            else:
                self.gap_result_label.config(text=f"Surplus: ${abs(gap):,.2f}", foreground='green')
                
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid numbers for cost and savings.")

    def create_products_tab(self, parent, product_text):
        """Creates the Recommended Products tab."""
        frame = ttk.Frame(parent, padding=15)
        
        label = ttk.Label(frame, text=product_text, wraplength=700, justify='left', font=('Arial', 11))
        label.pack(anchor='w')
        
        return frame

    def create_advisor_tab(self, parent, advisor_text):
        """Creates the Advisor connection tab."""
        frame = ttk.Frame(parent, padding=15)
        
        label = ttk.Label(frame, text=advisor_text, wraplength=700, justify='left')
        label.pack(anchor='w', pady=10)
        
        mock_button = ttk.Button(frame, text="Find a Certified Advisor (Mock Button)")
        mock_button.pack(pady=20)
        
        return frame


if __name__ == "__main__":
    root = tk.Tk()
    app = LifeEventPlannerApp(root)
    root.mainloop()