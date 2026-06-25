# minigame

**PROMPTS**

Actúa como un experto en Python y Tkinter. Crea un juego interactivo llamado "Papa o Bomba". El menú principal debe renderizar imágenes PNG directamente sobre un Canvas usando create_image con coordenadas específicas para simular interespaciado entre los botones, asegurando que no existan bordes ni recuadros grises de fondo alrededor de las imágenes transparentes. El juego debe incluir un tablero de 15 casillas con lógica para colocar 3 bombas ocultas y alternar turnos de ataque (Modo Versus Computadora y Modo Versus Amigo). Usa comentarios limpios solo para lógica crítica.

Optimiza las funciones de carga de imágenes de mi script de Tkinter. Necesito una función que resuelva las rutas de archivos de forma dinámica tanto en desarrollo local como si el script llega a ser compilado en un binario autónomo (usando sys._MEIPASS y os.path.abspath). Asegura que la construcción de rutas de la carpeta "images/" utilice os.path.join para garantizar total compatibilidad de separadores entre Windows, Linux y macOS.

Proporcióname los comandos exactos de terminal para macOS para instalar y ejecutar PyInstaller vinculándolo directamente al intérprete activo mediante "python3 -m". El comando de empaquetado debe generar un único archivo ejecutable autónomo (--onefile), ocultar la consola de comandos de fondo (--noconsole), e inyectar de manera explícita la carpeta de recursos "images" y las dependencias de datos del módulo nativo de tkinter (--collect-data).

**¿QUÉ SE PIDIO A LA IA?**

**Arreglar el menú del juego:** Quitar los botones y etiquetas de Tkinter porque dejaban un cuadro gris feo de fondo y amontonaban las imágenes, y ponerlas directamente sobre el fondo controlando el espacio entre ellas.
 
**Crear un archivo ejecutable autónomo:** Instalar y usar PyInstaller desde el propio intérprete de Python para empaquetar todo el juego con sus imágenes en un solo archivo, asegurando que el evaluador pueda abrirlo con doble clic sin configurar nada en su sistema.

**¿POR QUÉ SE AJUSTÓ O REFINÓ EL PROMPT?**

**Para corregir las rutas de las imágenes:** Crear una función automática para que el juego encuentre la carpeta `images` en cualquier computadora (Mac o Windows) sin dar errores de carpetas, ya sea ejecutando el archivo suelto o compilado.

**Solucionar el error de Tkinter en Mac:** Resolver el fallo de ejecución (`ModuleNotFoundError: No module named '_tkinter'`) instalando los componentes gráficos que le faltaban a Python en macOS.

**EVIDENCIA DE MEJORA**

**ESTADO INICIAL**

**Uso de Componentes:** Los botones del menú estaban montados utilizando contenedores estándar de la librería (tk.Label y tk.Button) incrustados sobre el Canvas.

**Fondo de los Botones:** Presentaba un recuadro gris sólido alrededor de los recursos gráficos, el cual bloqueaba y rompía visualmente la continuidad del fondo degradado del juego.

**Espaciado y Distribución:** Los elementos se mostraban amontonados debido a las restricciones físicas de la rejilla de Tkinter, impidiendo un interespaciado personalizado.

**Bordes e Interferencia:** Se visualizaban líneas de relieve y recuadros de enfoque activos al interactuar o mover el cursor sobre los botones.

**ESTADO OPTIMIZADO**

**Uso de Componentes:** Se eliminaron los elementos de interfaz genéricos y se renderizaron los recursos PNG de forma nativa utilizando directamente el método Canvas.create_image.

**Fondo de los Botones:** Transparencia real mediante el canal alfa del archivo PNG, logrando que las imágenes de los botones se fusionen perfectamente sobre el fondo sin marcos de ningún tipo.Espaciado y Distribución: Distribución matemática exacta basada en coordenadas de píxeles en el eje vertical ($y$), garantizando una separación uniforme y limpia entre cada opción del menú.

**Bordes e Interferencia:** Cero bordes y eliminación absoluta de cualquier relieve del sistema operativo, dejando el diseño limpio para la interacción.

**EXPLICACIÓN DE CÓMO SE PROBÓ EL CÓDIGO**
Corriendo desde la terminal de VS CODE y usando el interprete de Python estuve testeando y haciendo modificaciones en el código.

**LIMITACIONES**

**Falta de componentes gráficos nativos en el entorno local:** El intérprete de Python instalado en mi computadora MacOs a través de Homebrew no incluye por defecto la librería tkinter, lo que causó un error crítico de ejecución (ModuleNotFoundError: No module named '_tkinter') al intentar correr el script desde una terminal limpia.

**¿QUÉ APRENDÍ USANDO LA IA PARA PROGRAMAR?**

No es la primera vez que pruebo hacer Vibecoding, siempre aprendo algo nuevo, ya sea una nueva o mejor forma de dar las instrucciones para optimizar código propio o iniciar algo desde cero, sin embargo, me gusta ir chequeando y leyendo todo lo nuevo que voy incluyendo, me ayuda a comprender mejor el código, corregir errores sin apoyo de la IA, y en muchas ocasiones poder hacer ajustes por mi cuenta sin depender de la IA para optimizar mis tokens y/o recursos.

**VENTAJAS Y LIMITES DEL VIBECODING EN ESTE PROYECTO**

**VENTAJAS:** Siento que la mayor ventaja fue la optimización del proyecto como tal, con el prompt bien detallado el asistente logro comprender de inmediato y traducir mi idea hacia el código, en algunas ocasiones el agente divago, pero por eso use el criterio personal también para realizar las correciones correctas.

De igual forma 


