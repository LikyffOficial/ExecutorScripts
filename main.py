cat > main.py << 'EOF'
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.utils import platform

import threading
import traceback
import time

if platform == 'android':
    from android.permissions import request_permissions, Permission
    from android import mActivity
    from jnius import autoclass
    
    Intent = autoclass('android.content.Intent')
    Settings = autoclass('android.provider.Settings')
    Uri = autoclass('android.net.Uri')
    Context = autoclass('android.content.Context')


class ScriptExecutor:
    """Executa scripts Python em background"""
    
    def __init__(self, output_callback=None):
        self.is_running = False
        self.thread = None
        self.output_callback = output_callback
        self.stop_flag = False
        
    def run_script(self, script_code):
        """Executa o script em uma thread separada"""
        if self.is_running:
            self.output("❌ Script já está rodando!")
            return
            
        self.stop_flag = False
        self.is_running = True
        self.thread = threading.Thread(target=self._execute, args=(script_code,))
        self.thread.daemon = True
        self.thread.start()
    
    def _execute(self, script_code):
        """Execução interna do script"""
        try:
            self.output("🚀 Iniciando script...")
            
            # Contexto de execução com funções úteis
            exec_globals = {
                'output': self.output,
                'sleep': time.sleep,
                'stop_flag': lambda: self.stop_flag,
            }
            
            exec(script_code, exec_globals)
            
            if not self.stop_flag:
                self.output("✅ Script concluído!")
        except Exception as e:
            self.output(f"❌ Erro: {str(e)}\n{traceback.format_exc()}")
        finally:
            self.is_running = False
    
    def stop_script(self):
        """Sinaliza para parar a execução"""
        self.stop_flag = True
        self.is_running = False
        self.output("⏹ Script parado pelo usuário")
    
    def output(self, message):
        """Envia mensagem para o callback"""
        if self.output_callback:
            Clock.schedule_once(lambda dt: self.output_callback(message))


class ExecutorScriptsApp(App):
    """Aplicativo principal"""
    
    def build(self):
        self.title = "🤖 Executor de Scripts"
        self.executor = ScriptExecutor(output_callback=self.on_script_output)
        
        # Layout principal
        main_layout = BoxLayout(
            orientation='vertical',
            padding=15,
            spacing=10
        )
        
        # Cabeçalho
        header = Label(
            text='🤖 EXECUTOR DE SCRIPTS v1.0',
            size_hint_y=0.08,
            font_size='18sp',
            bold=True,
            color=(0.2, 0.8, 0.2, 1)
        )
        main_layout.add_widget(header)
        
        # Área de entrada do script
        script_label = Label(
            text='📝 Cole seu script Python:',
            size_hint_y=0.05,
            font_size='14sp',
            halign='left'
        )
        main_layout.add_widget(script_label)
        
        self.script_input = TextInput(
            hint_text='# Exemplo:\n# for i in range(5):\n#     output(f"Contagem: {i}")\n#     sleep(1)',
            size_hint_y=0.35,
            multiline=True,
            font_name='RobotoMono-Regular',
            font_size='13sp',
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(0.9, 0.9, 0.9, 1)
        )
        main_layout.add_widget(self.script_input)
        
        # Botões de controle
        controls = BoxLayout(
            size_hint_y=0.1,
            spacing=10
        )
        
        self.play_btn = Button(
            text='▶️ EXECUTAR',
            background_color=(0.2, 0.7, 0.2, 1),
            font_size='15sp',
            bold=True
        )
        self.play_btn.bind(on_press=self.on_play)
        
        self.stop_btn = Button(
            text='⏹ PARAR',
            background_color=(0.8, 0.2, 0.2, 1),
            font_size='15sp',
            bold=True,
            disabled=True
        )
        self.stop_btn.bind(on_press=self.on_stop)
        
        perms_btn = Button(
            text='⚙️ CONFIG',
            background_color=(0.2, 0.5, 0.8, 1),
            font_size='15sp',
            bold=True
        )
        perms_btn.bind(on_press=self.on_settings)
        
        controls.add_widget(self.play_btn)
        controls.add_widget(self.stop_btn)
        controls.add_widget(perms_btn)
        
        main_layout.add_widget(controls)
        
        # Área de output
        output_label = Label(
            text='📊 Console de Saída:',
            size_hint_y=0.05,
            font_size='14sp',
            halign='left'
        )
        main_layout.add_widget(output_label)
        
        self.output_display = TextInput(
            text='💡 Pronto para executar scripts!\n',
            size_hint_y=0.37,
            readonly=True,
            multiline=True,
            font_size='12sp',
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(0.3, 1, 0.3, 1)
        )
        main_layout.add_widget(self.output_display)
        
        # Solicita permissões ao iniciar
        if platform == 'android':
            Clock.schedule_once(lambda dt: self.request_permissions(), 1)
        
        return main_layout
    
    def request_permissions(self):
        """Solicita permissões necessárias"""
        try:
            permissions = [
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE,
            ]
            request_permissions(permissions)
            self.on_script_output("✅ Permissões solicitadas")
        except Exception as e:
            self.on_script_output(f"⚠️ Erro ao solicitar permissões: {e}")
    
    def on_play(self, instance):
        """Executa o script"""
        script = self.script_input.text.strip()
        
        if not script:
            self.on_script_output("❌ Cole um script primeiro!")
            return
        
        if script.startswith('#'):
            # Remove linhas de comentário do exemplo
            lines = [l for l in script.split('\n') if l.strip() and not l.strip().startswith('#')]
            if not lines:
                self.on_script_output("❌ Script vazio! Remova apenas os comentários de exemplo.")
                return
        
        # Desabilita botão play, habilita stop
        self.play_btn.disabled = True
        self.stop_btn.disabled = False
        
        self.executor.run_script(script)
    
    def on_stop(self, instance):
        """Para o script"""
        self.executor.stop_script()
        self.play_btn.disabled = False
        self.stop_btn.disabled = True
    
    def on_settings(self, instance):
        """Abre configurações"""
        self.on_script_output("⚙️ Abrindo configurações do sistema...")
        
        if platform == 'android':
            try:
                intent = Intent(Settings.ACTION_SETTINGS)
                mActivity.startActivity(intent)
            except Exception as e:
                self.on_script_output(f"❌ Erro: {e}")
        else:
            self.on_script_output("⚠️ Disponível apenas no Android")
    
    def on_script_output(self, message):
        """Adiciona mensagem ao console"""
        timestamp = time.strftime("%H:%M:%S")
        self.output_display.text += f"[{timestamp}] {message}\n"
        
        # Auto-scroll para o final
        self.output_display.cursor = (0, len(self.output_display.text))
        
        # Re-habilita botões se o script terminou
        if "concluído" in message.lower() or "erro" in message.lower() or "parado" in message.lower():
            self.play_btn.disabled = False
            self.stop_btn.disabled = True


if __name__ == '__main__':
    ExecutorScriptsApp().run()
EOF
