import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time



# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas."""
    
    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:

    # 1 Configurar la dirección
    from_field = (By.ID, 'from')  # Campo "Desde"
    to_field = (By.ID, 'to')  # Campo "Hasta"

    # 2.1 Botón para iniciar la selección de tarifa
    request_taxi_button = (By.XPATH, "//button[contains(text(), 'Pedir un taxi')]")

    # 2.2 Seleccionar la tarifa Comfort 
    comfort_tariff = (By.XPATH, "//div[contains(@class, 'tcard') and .//div[text()='Comfort']]")

    # 3.1 Rellenar el número de teléfono
    phone_button = (By.CLASS_NAME, "np-button")  # Botón para activar el campo del número de teléfono
    phone_field = (By.ID, "phone")  # Número de teléfono
    next_button = (By.CLASS_NAME, "button.full")  # Botón "Siguiente" para confirmar el número

    # 3.2 Campo del código SMS y botón de cierre
    sms_code_field = (By.ID, "code")  # Campo para ingresar el código SMS
    close_sms_modal = (By.XPATH, "//button[contains(@class, 'close-button') and contains(@class, 'section-close')]")  #botón de cierre

    # 4.1 Botón para método de pago
    payment_method_button = (By.XPATH, "//div[contains(@class, 'pp-button') and contains(@class, 'filled')]")

    # 4.2 Botón para agregar una tarjeta con el botón +
    add_card_button = (By.CLASS_NAME, "pp-plus-container")

    # 4.3 Agregar una tarjeta de crédito
    card_number_field = (By.ID, "number")  # Campo Número de Tarjeta
    cvv_field = (By.ID, "code")  # Campo CVV # Campo CVV
    confirm_card_button = (By.XPATH, "//button[@type='submit' and text()='Agregar']")





    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(10)  # Espera global para evitar errores de carga

    def set_from(self, from_address):
        """Ingresa la dirección de origen"""
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.from_field))
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        """Ingresa la dirección de destino"""
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.to_field))
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        """Obtiene el valor del campo 'Desde'"""
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.from_field))
        return self.driver.find_element(*self.from_field).get_attribute("value")
    
    def get_to(self):
        """Obtiene el valor del campo 'Hasta'"""
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.to_field))
        return self.driver.find_element(*self.to_field).get_attribute("value")
    
    def select_comfort_tariff(self):
        """Hace clic en 'Pedir un taxi' y luego selecciona la tarifa Comfort."""

        # 1 Hacer clic en "Pedir un taxi"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.request_taxi_button)
        ).click()

        # 2 Esperar a que la tarifa Comfort sea clickeable
        comfort_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.comfort_tariff)
        )

        # 3 Hacer scroll hasta el botón para asegurarnos de que sea visible
        self.driver.execute_script("arguments[0].scrollIntoView();", comfort_button)

        # 4 Hacer clic en la tarifa Comfort
        comfort_button.click()

        # 5 Confirmar que la selección se hizo correctamente
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'tcard active') and .//div[text()='Comfort']]"))
        )

    def enter_phone_number(self, phone_number):
        """Hace clic en 'Número de teléfono' y lo ingresa en el campo correspondiente."""

        # 1 Hacer clic en el botón "Número de teléfono"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.phone_button)
        ).click()

        # 2 Esperar a que el campo de teléfono sea interactuable
        phone_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.phone_field)
        )

        # 3 Escribir el número
        phone_input.send_keys(phone_number)
        phone_input.send_keys(Keys.TAB)  # Simular cambio de foco para activar el siguiente paso  

        # 4 Hacer clic en "Siguiente" para confirmar el número y llevarte al código
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.next_button)
        ).click()

        # 5 Esperar a que aparezca el campo de código SMS
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.sms_code_field)
        )

        # 6 Ingresar el código SMS (por ahora, un valor de prueba)
        self.driver.find_element(*self.sms_code_field).send_keys("1234")

        # 7Esperar a que el botón de cierre sea interactuable
        close_button = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located(self.close_sms_modal)
    )

        # 8 Forzar el clic con JS ya que puede haber nuevamente errores con elementos superpuestos
        self.driver.execute_script("arguments[0].click();", close_button)

        # 9 Esperar medio segundo para asegurar que la página procese el cierre
        time.sleep(0.5)

    def open_payment_method(self):
        """Hace clic en 'Método de pago' antes de agregar una tarjeta."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.payment_method_button)
        ).click()

    def click_add_card_button(self):
        """Hace clic en el botón '+' para agregar una nueva tarjeta."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_card_button)
        ).click()


    def add_credit_card(self, card_number, cvv):
        """Ingresa los datos de la tarjeta de crédito y confirma la tarjeta."""

        # 1️⃣ Esperar hasta que el campo de número de tarjeta sea visible e interactuable
        card_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.card_number_field)
        )
        
        # 2️⃣ Limpiar y escribir el número de tarjeta
        card_input.clear()
        card_input.send_keys(card_number)
        print(f"✅ Número de tarjeta enviado: {card_number}")
        time.sleep(1)

        # 3️⃣ Verificar en qué campo estamos escribiendo
        actual_value = self.driver.execute_script("return arguments[0].value;", card_input)
        print(f"🔍 Verificación: Número en campo de tarjeta después de escribir: {actual_value}")

        # 4️⃣ Asegurar que el campo CVV esté accesible
        cvv_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.cvv_field)
        )
        print("✅ Campo CVV encontrado")

        # 5️⃣ Intentar hacer clic en el campo CVV
        try:
            cvv_input.click()
            print("✅ Clic en CVV realizado")
        except:
            self.driver.execute_script("arguments[0].click();", cvv_input)
            print("✅ Clic en CVV realizado con JavaScript.")

        time.sleep(1)  # Espera para asegurar que el campo está activado

        # 6️⃣ Intentar escribir el CVV manualmente
        try:
            cvv_input.clear()
            cvv_input.send_keys(cvv)
            print(f"✅ CVV escrito: {cvv}")
        except:
            self.driver.execute_script("arguments[0].value = arguments[1];", cvv_input, cvv)
            print(f"✅ CVV escrito con JavaScript: {cvv}")

        # 7️⃣ Simular eventos para cambiar el foco y activar el botón "Agregar"
        cvv_input.send_keys(Keys.TAB)  # Mueve el foco al siguiente campo
        time.sleep(1)
        self.driver.execute_script("arguments[0].blur();", cvv_input)  # Simular pérdida de foco
        print("✅ Simulación de TAB y pérdida de foco realizada")

        # 8️⃣ Esperar a que el botón "Agregar" se active
        add_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.confirm_card_button)
        )
        print("✅ Botón 'Agregar' activado.")

        # 9️⃣ Hacer clic en "Agregar"
        try:
            add_button.click()
            print("✅ Tarjeta agregada correctamente")
        except:
            self.driver.execute_script("arguments[0].click();", add_button)
            print("✅ Clic en botón 'Agregar' realizado con JavaScript")


class TestUrbanRoutes:

    driver = None  # Definir el driver a nivel de clase

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}

        # Convertimos capabilities en options para evitar el error
        chrome_options = Options()
        for key, value in capabilities.items():
            chrome_options.set_capability(key, value)

        # Usamos Service() para evitar problemas de compatibilidad
        service = Service()
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)


    def test_full_taxi_order(self):
        """Prueba automatizada para pedir un taxi en Urban Routes."""
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # 1 Configurar la dirección
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)

        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

        # 2 Seleccionar tarifa Comfort
        routes_page.select_comfort_tariff()

        # 3 Rellenar el número de teléfono
        phone_number = data.phone_number
        routes_page.enter_phone_number(phone_number)

        # 4 Método de pago para agregar tarjeta
        routes_page.open_payment_method() #Abrir método de pago
        routes_page.click_add_card_button() # Hacer clic en el botón "+" para agregar una nueva tarjeta

        # 4.1 Agregar tarjeta de crédito 
        card_number = data.card_number
        card_code = data.card_code

        # Usar add_credit_card() en lugar de enter_card_number() y enter_card_cvv_and_confirm()
        routes_page.add_credit_card(card_number, card_code)

        print(f"DEBUG: Enviando tarjeta: {card_number}, CVV: {card_code}")

        routes_page.add_credit_card(card_number, card_code)  # Llamar la función correcta

    @classmethod
    def teardown_class(cls):
        """Cierra el navegador después de ejecutar las pruebas"""
        cls.driver.quit()



