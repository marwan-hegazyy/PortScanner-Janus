import socket
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.prompt import Prompt
from rich.align import Align  # تم استيراد Align للمحاذاة الصحيحة

console = Console()

def create_layout(ip="", start_p="", end_p="", results=""):
    layout = Layout()
    
    # تقسيم الشاشة إلى 4 أقسام راسية: IP، نطاق البورتات، النتائج، والـ Footer
    layout.split_column(
        Layout(name="top", size=3),
        Layout(name="middle", size=3),
        Layout(name="bottom", ratio=1),
        Layout(name="footer", size=1)
    )
    
    # مربع الـ IP
    layout["top"].update(Panel(f"[bold cyan]{ip}[/bold cyan]", title="عنوان الـ IP", border_style="green"))
    
    # مربع نطاق البورتات
    layout["middle"].split_row(
        Layout(Panel(f"[bold yellow]{start_p}[/bold yellow]", title="رقم نهاية البورت", border_style="blue")),
        Layout(Panel(f"[bold yellow]{end_p}[/bold yellow]", title="رقم بداية البورت", border_style="blue"))
    )
    
    # مربع البورتات المفتوحة
    layout["bottom"].update(Panel(results, title="البورتات المفتوحة", border_style="magenta"))
    
    # محاذاة الاسم لليمين باستخدام Align.right
    layout["footer"].update(Align.right("[bold white]Create Wiht {Janus}[/bold white]"))
    
    return layout

def main():
    console.clear()
    
    # أخذ المدخلات من المستخدم
    target_ip = Prompt.ask("[bold green]أدخل عنوان الـ IP[/bold green]")
    start_port = int(Prompt.ask("[bold blue]أدخل رقم بداية البورت[/bold blue]"))
    end_port = int(Prompt.ask("[bold blue]أدخل رقم نهاية البورت[/bold blue]"))

    open_ports = []
    
    console.clear()
    console.print("[bold yellow]جاري فحص المنافذ...[/bold yellow]\n")

    # حلقة الفحص
    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            open_ports.append(f"Port {port} is OPEN")
        s.close()

    # تجهيز النتيجة للعرض
    if open_ports:
        results_text = "\n".join([f"[bold green]✔ {p}[/bold green]" for p in open_ports])
    else:
        results_text = "[bold red]لا توجد بورتات مفتوحة في هذا النطاق.[/bold red]"

    # عرض الواجهة النهائية
    console.clear()
    final_layout = create_layout(target_ip, str(start_port), str(end_port), results_text)
    console.print(final_layout)

if __name__ == "__main__":
    main()
