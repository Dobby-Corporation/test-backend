const VKID = window.VKIDSDK;

const config = JSON.parse($('#config').text());

VKID.Config.init({
    app: 53004573,
    redirectUrl: 'http://localhost',
    // mode: VKID.ConfigAuthMode.Redirect,
    responseMode: VKID.ConfigResponseMode.Callback,
});

$('.auth-login').on('click', () => {
    const floatingOneTap = new VKID.FloatingOneTap();

    floatingOneTap.render({
        appName: 'Test Booster',
        showAlternativeLogin: true
    })
    .on(VKID.WidgetEvents.ERROR, vkidOnError)
    .on(VKID.FloatingOneTapInternalEvents.LOGIN_SUCCESS, function (payload) {
        alert("LOGIN_SUCCESS!");
    })
    .on(VKID.FloatingOneTapInternalEvents.SHOW_FULL_AUTH, function () {
        alert("SHOW_FULL_AUTH");
    })
    .on(VKID.FloatingOneTapInternalEvents.START_AUTHORIZE, function () {
        alert("START_AUTHORIZE");
    });

    function vkidOnSuccess(data) {
        floatingOneTap.close();
        // Обработка полученного результата
    }

    function vkidOnError(error) {
        // Обработка ошибки
    }
});