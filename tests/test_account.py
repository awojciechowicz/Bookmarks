import pytest
from playwright.sync_api import Page, expect


# ---------------------------------------------------------------------------
# Testy strony logowania
# ---------------------------------------------------------------------------

def test_login_page_loads(page: Page, live_server):
    """Sprawdza, czy strona logowania się ładuje poprawnie."""
    page.goto(f"{live_server.url}/account/login/")
    expect(page).to_have_title("Logowanie")
    expect(page.locator("h1")).to_have_text("Logowanie")


def test_login_form_visible(page: Page, live_server):
    """Sprawdza, czy formularz logowania zawiera wymagane pola."""
    page.goto(f"{live_server.url}/account/login/")
    expect(page.locator("input[name='username']")).to_be_visible()
    expect(page.locator("input[name='password']")).to_be_visible()
    expect(page.locator("input[type='submit']")).to_be_visible()


@pytest.mark.django_db
def test_login_success(page: Page, live_server, test_user):
    """Sprawdza pomyślne logowanie i przekierowanie do dashboardu."""
    page.goto(f"{live_server.url}/account/login/")
    page.fill("input[name='username']", "testuser")
    page.fill("input[name='password']", "TestPassword123")
    page.click("input[type='submit']")

    # Po zalogowaniu powinniśmy trafić na dashboard
    expect(page).to_have_url(f"{live_server.url}/")


@pytest.mark.django_db
def test_login_invalid_credentials(page: Page, live_server):
    """Sprawdza, czy błędne dane logowania wyświetlają komunikat o błędzie."""
    page.goto(f"{live_server.url}/account/login/")
    page.fill("input[name='username']", "zly_uzytkownik")
    page.fill("input[name='password']", "zlehaslo")
    page.click("input[type='submit']")

    # Formularz powinien pokazać błąd i pozostać na stronie logowania
    expect(page.locator("text=Nieprawidłowa nazwa użytkownika lub hasło")).to_be_visible()


# ---------------------------------------------------------------------------
# Testy strony rejestracji
# ---------------------------------------------------------------------------

def test_register_page_loads(page: Page, live_server):
    """Sprawdza, czy strona rejestracji się ładuje."""
    page.goto(f"{live_server.url}/account/register/")
    expect(page.locator("h1")).to_be_visible()


def test_register_link_on_login_page(page: Page, live_server):
    """Sprawdza, czy link do rejestracji działa ze strony logowania."""
    page.goto(f"{live_server.url}/account/login/")
    page.click("text=zarejestruj sie tutaj")
    expect(page).to_have_url(f"{live_server.url}/account/register/")


@pytest.mark.django_db
def test_register_new_user(page: Page, live_server):
    """Sprawdza, czy rejestracja nowego użytkownika przebiega poprawnie."""
    page.goto(f"{live_server.url}/account/register/")
    page.fill("input[name='username']", "nowy_uzytkownik")
    page.fill("input[name='email']", "nowy@example.com")
    page.fill("input[name='password']", "BezpieczneHaslo123")
    page.fill("input[name='password2']", "BezpieczneHaslo123")
    page.click("input[type='submit']")

    # Po rejestracji powinna pojawić się strona potwierdzenia
    expect(page.locator("text=nowy_uzytkownik")).to_be_visible()


# ---------------------------------------------------------------------------
# Testy przekierowania nieuwierzytelnionego użytkownika
# ---------------------------------------------------------------------------

def test_dashboard_redirects_to_login(page: Page, live_server):
    """Sprawdza, czy niezalogowany użytkownik jest przekierowywany do logowania."""
    page.goto(f"{live_server.url}/")
    expect(page).to_have_url(f"{live_server.url}/account/login/?next=/")
