import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
from typing import List, Dict, Optional

class AgriculturalProduct:
    """农产品类"""
    def __init__(self, product_id: int, name: str, category: str, price: float, stock: float, unit: str):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.unit = unit

class SaleRecord:
    """销售记录类"""
    def __init__(self, record_id: int, product_id: int, product_name: str, quantity: float, total_price: float, sale_date: str, customer: str):
        self.record_id = record_id
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.total_price = total_price
        self.sale_date = sale_date
        self.customer = customer

class AgriculturalSalesManager:
    """农产品销售管理器（内存版本）"""
    
    def __init__(self):
        self.products: List[AgriculturalProduct] = []
        self.sales_records: List[SaleRecord] = []
        self.next_product_id = 1
        self.next_record_id = 1
        self.init_sample_data()
    
    def init_sample_data(self):
        """初始化示例数据"""
        sample_products = [
            ('有机苹果', '水果', 8.5, 100, '斤'),
            ('绿色蔬菜', '蔬菜', 6.0, 50, '斤'),
            ('农家鸡蛋', '禽蛋', 12.0, 200, '个'),
            ('优质大米', '粮食', 3.5, 500, '斤'),
            ('新鲜玉米', '蔬菜', 2.5, 80, '斤'),
            ('土鸡', '禽肉', 25.0, 30, '只')
        ]
        
        for name, category, price, stock, unit in sample_products:
            self.add_product(name, category, price, stock, unit)
    
    def add_product(self, name: str, category: str, price: float, stock: float, unit: str) -> bool:
        """添加新产品"""
        try:
            product = AgriculturalProduct(self.next_product_id, name, category, price, stock, unit)
            self.products.append(product)
            self.next_product_id += 1
            return True
        except Exception as e:
            print(f"添加产品失败: {e}")
            return False
    
    def get_all_products(self) -> List[AgriculturalProduct]:
        """获取所有产品"""
        return self.products
    
    def find_product_by_id(self, product_id: int) -> Optional[AgriculturalProduct]:
        """根据ID查找产品"""
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None
    
    def update_product_stock(self, product_id: int, new_stock: float) -> bool:
        """更新产品库存"""
        product = self.find_product_by_id(product_id)
        if product:
            product.stock = new_stock
            return True
        return False
    
    def make_sale(self, product_id: int, quantity: float, customer: str = "零售客户") -> bool:
        """进行销售"""
        try:
            product = self.find_product_by_id(product_id)
            if not product:
                return False
            
            if product.stock < quantity:
                return False
            
            total_price = product.price * quantity
            new_stock = product.stock - quantity
            
            # 创建销售记录
            sale_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record = SaleRecord(
                self.next_record_id, product_id, product.name, 
                quantity, total_price, sale_date, customer
            )
            self.sales_records.append(record)
            self.next_record_id += 1
            
            # 更新库存
            product.stock = new_stock
            return True
            
        except Exception as e:
            print(f"销售失败: {e}")
            return False
    
    def get_sales_records(self, days: int = 30) -> List[SaleRecord]:
        """获取销售记录"""
        if days <= 0:
            return self.sales_records
        
        cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=days)).timestamp()
        recent_records = []
        
        for record in self.sales_records:
            record_date = datetime.datetime.strptime(record.sale_date, "%Y-%m-%d %H:%M:%S").timestamp()
            if record_date >= cutoff_date:
                recent_records.append(record)
        
        return recent_records
    
    def get_sales_statistics(self) -> Dict:
        """获取销售统计"""
        total_revenue = sum(record.total_price for record in self.sales_records)
        
        # 今日销售额
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        today_revenue = sum(
            record.total_price for record in self.sales_records 
            if record.sale_date.startswith(today)
        )
        
        # 最畅销产品
        product_sales = {}
        for record in self.sales_records:
            if record.product_name not in product_sales:
                product_sales[record.product_name] = {
                    'quantity': 0,
                    'revenue': 0
                }
            product_sales[record.product_name]['quantity'] += record.quantity
            product_sales[record.product_name]['revenue'] += record.total_price
        
        best_seller = None
        if product_sales:
            best_product = max(product_sales.items(), key=lambda x: x[1]['revenue'])
            best_seller = (best_product[0], best_product[1]['quantity'], best_product[1]['revenue'])
        
        return {
            'total_revenue': total_revenue,
            'today_revenue': today_revenue,
            'best_seller': best_seller,
            'product_sales': product_sales
        }

class AgriculturalSalesApp:
    """农产品销售管理应用"""
    
    def __init__(self, root):
        self.root = root
        self.manager = AgriculturalSalesManager()
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        self.root.title("农产品销售管理系统")
        self.root.geometry("800x600")
        
        # 创建标签页
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 产品管理标签页
        products_frame = ttk.Frame(notebook)
        notebook.add(products_frame, text="产品管理")
        self.setup_products_tab(products_frame)
        
        # 销售管理标签页
        sales_frame = ttk.Frame(notebook)
        notebook.add(sales_frame, text="销售管理")
        self.setup_sales_tab(sales_frame)
        
        # 销售记录标签页
        records_frame = ttk.Frame(notebook)
        notebook.add(records_frame, text="销售记录")
        self.setup_records_tab(records_frame)
        
        # 统计报表标签页
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="统计报表")
        self.setup_stats_tab(stats_frame)
    
    def setup_products_tab(self, parent):
        """设置产品管理标签页"""
        # 工具栏
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(toolbar, text="添加产品", command=self.add_product_dialog).pack(side='left', padx=5)
        ttk.Button(toolbar, text="刷新列表", command=self.refresh_products).pack(side='left', padx=5)
        
        # 产品列表
        columns = ('ID', '名称', '类别', '价格', '库存', '单位')
        self.products_tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        # 设置列标题
        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=100)
        
        self.products_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # 初始加载数据
        self.refresh_products()
    
    def setup_sales_tab(self, parent):
        """设置销售管理标签页"""
        # 销售表单
        form_frame = ttk.LabelFrame(parent, text="销售信息", padding=10)
        form_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(form_frame, text="选择产品:").grid(row=0, column=0, sticky='w', pady=5)
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(form_frame, textvariable=self.product_var, state='readonly')
        self.product_combo.grid(row=0, column=1, sticky='ew', pady=5, padx=5)
        
        ttk.Label(form_frame, text="销售数量:").grid(row=1, column=0, sticky='w', pady=5)
        self.quantity_entry = ttk.Entry(form_frame)
        self.quantity_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=5)
        
        ttk.Label(form_frame, text="客户名称:").grid(row=2, column=0, sticky='w', pady=5)
        self.customer_entry = ttk.Entry(form_frame)
        self.customer_entry.insert(0, "零售客户")
        self.customer_entry.grid(row=2, column=1, sticky='ew', pady=5, padx=5)
        
        ttk.Button(form_frame, text="执行销售", command=self.make_sale).grid(row=3, column=0, columnspan=2, pady=10)
        
        # 产品库存信息
        info_frame = ttk.LabelFrame(parent, text="产品库存信息", padding=10)
        info_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        columns = ('ID', '名称', '类别', '价格', '库存', '单位')
        self.sales_products_tree = ttk.Treeview(info_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.sales_products_tree.heading(col, text=col)
            self.sales_products_tree.column(col, width=100)
        
        self.sales_products_tree.pack(fill='both', expand=True)
        
        # 绑定产品选择事件
        self.product_combo.bind('<<ComboboxSelected>>', self.on_product_selected)
        
        self.refresh_sales_products()
    
    def setup_records_tab(self, parent):
        """设置销售记录标签页"""
        # 工具栏
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(toolbar, text="查看最近").pack(side='left', padx=5)
        self.days_var = tk.StringVar(value="30")
        days_combo = ttk.Combobox(toolbar, textvariable=self.days_var, values=["7", "30", "90", "0"], width=5, state='readonly')
        days_combo.pack(side='left', padx=5)
        ttk.Label(toolbar, text="天的记录").pack(side='left', padx=5)
        ttk.Button(toolbar, text="刷新", command=self.refresh_records).pack(side='left', padx=10)
        
        # 记录列表
        columns = ('日期', '产品', '数量', '总价', '客户')
        self.records_tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.records_tree.heading(col, text=col)
            self.records_tree.column(col, width=120)
        
        self.records_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.refresh_records()
    
    def setup_stats_tab(self, parent):
        """设置统计报表标签页"""
        # 统计信息框架
        stats_frame = ttk.Frame(parent)
        stats_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.stats_text = tk.Text(stats_frame, height=20, width=80)
        scrollbar = ttk.Scrollbar(stats_frame, orient='vertical', command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=scrollbar.set)
        
        self.stats_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        ttk.Button(parent, text="刷新统计", command=self.refresh_stats).pack(pady=10)
        
        self.refresh_stats()
    
    def refresh_products(self):
        """刷新产品列表"""
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        for product in self.manager.get_all_products():
            self.products_tree.insert('', 'end', values=(
                product.product_id, product.name, product.category, 
                f"{product.price:.2f}", f"{product.stock:.1f}", product.unit
            ))
    
    def refresh_sales_products(self):
        """刷新销售页面的产品列表"""
        # 更新下拉框
        products = self.manager.get_all_products()
        product_names = [f"{p.product_id}. {p.name} (库存: {p.stock}{p.unit})" for p in products]
        self.product_combo['values'] = product_names
        
        # 更新树形视图
        for item in self.sales_products_tree.get_children():
            self.sales_products_tree.delete(item)
        
        for product in products:
            self.sales_products_tree.insert('', 'end', values=(
                product.product_id, product.name, product.category, 
                f"{product.price:.2f}", f"{product.stock:.1f}", product.unit
            ))
    
    def refresh_records(self):
        """刷新销售记录"""
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        
        try:
            days = int(self.days_var.get())
        except:
            days = 30
            
        records = self.manager.get_sales_records(days)
        
        for record in records:
            self.records_tree.insert('', 'end', values=(
                record.sale_date, record.product_name, 
                f"{record.quantity:.1f}", f"{record.total_price:.2f}", record.customer
            ))
    
    def refresh_stats(self):
        """刷新统计信息"""
        stats = self.manager.get_sales_statistics()
        
        self.stats_text.delete(1.0, tk.END)
        
        self.stats_text.insert(tk.END, "=== 销售统计报表 ===\n\n")
        self.stats_text.insert(tk.END, f"总销售额: {stats['total_revenue']:.2f} 元\n")
        self.stats_text.insert(tk.END, f"今日销售额: {stats['today_revenue']:.2f} 元\n\n")
        
        if stats['best_seller']:
            name, quantity, revenue = stats['best_seller']
            self.stats_text.insert(tk.END, f"最畅销产品: {name}\n")
            self.stats_text.insert(tk.END, f"总销量: {quantity:.1f}\n")
            self.stats_text.insert(tk.END, f"总销售额: {revenue:.2f} 元\n\n")
        
        self.stats_text.insert(tk.END, "=== 各产品销售情况 ===\n\n")
        for product_name, sales_data in stats['product_sales'].items():
            self.stats_text.insert(tk.END, 
                f"{product_name}: 销量 {sales_data['quantity']:.1f}, "
                f"销售额 {sales_data['revenue']:.2f} 元\n"
            )
    
    def add_product_dialog(self):
        """添加产品对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加新产品")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="产品名称:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        name_entry = ttk.Entry(dialog)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Label(dialog, text="产品类别:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        category_entry = ttk.Entry(dialog)
        category_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Label(dialog, text="价格:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        price_entry = ttk.Entry(dialog)
        price_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Label(dialog, text="库存:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        stock_entry = ttk.Entry(dialog)
        stock_entry.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Label(dialog, text="单位:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        unit_entry = ttk.Entry(dialog)
        unit_entry.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
        
        def save_product():
            try:
                name = name_entry.get().strip()
                category = category_entry.get().strip()
                price = float(price_entry.get())
                stock = float(stock_entry.get())
                unit = unit_entry.get().strip()
                
                if not all([name, category, unit]):
                    messagebox.showerror("错误", "请填写所有字段")
                    return
                
                if self.manager.add_product(name, category, price, stock, unit):
                    messagebox.showinfo("成功", "产品添加成功！")
                    self.refresh_products()
                    self.refresh_sales_products()
                    dialog.destroy()
                else:
                    messagebox.showerror("错误", "产品添加失败！")
                    
            except ValueError:
                messagebox.showerror("错误", "价格和库存必须是数字！")
        
        ttk.Button(dialog, text="保存", command=save_product).grid(row=5, column=0, columnspan=2, pady=10)
    
    def on_product_selected(self, event):
        """产品选择事件"""
        selection = self.product_var.get()
        if selection and '.' in selection:
            product_id = int(selection.split('.')[0])
            product = self.manager.find_product_by_id(product_id)
            if product:
                self.quantity_entry.delete(0, tk.END)
                self.quantity_entry.insert(0, "1")
    
    def make_sale(self):
        """执行销售"""
        selection = self.product_var.get()
        if not selection:
            messagebox.showerror("错误", "请选择产品！")
            return
        
        try:
            product_id = int(selection.split('.')[0])
            quantity = float(self.quantity_entry.get())
            customer = self.customer_entry.get().strip() or "零售客户"
            
            if quantity <= 0:
                messagebox.showerror("错误", "销售数量必须大于0！")
                return
            
            product = self.manager.find_product_by_id(product_id)
            if not product:
                messagebox.showerror("错误", "产品不存在！")
                return
            
            if self.manager.make_sale(product_id, quantity, customer):
                messagebox.showinfo("成功", f"销售成功！\n总金额: {product.price * quantity:.2f}元")
                self.refresh_sales_products()
                self.refresh_records()
                self.refresh_stats()
                # 清空输入
                self.quantity_entry.delete(0, tk.END)
                self.quantity_entry.insert(0, "1")
            else:
                messagebox.showerror("错误", f"销售失败！库存不足，当前库存: {product.stock}{product.unit}")
                
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字！")

def main():
    """主函数"""
    root = tk.Tk()
    app = AgriculturalSalesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()