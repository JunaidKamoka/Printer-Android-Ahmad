package printer.smart.app.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val HpBlue = Color(0xFF0096D6)
private val HpDark = Color(0xFF003F6B)
private val HpLight = Color(0xFFE6F4FB)

private val LightColors = lightColorScheme(
    primary = HpBlue,
    onPrimary = Color.White,
    primaryContainer = HpLight,
    onPrimaryContainer = HpDark,
    secondary = HpDark,
    background = Color(0xFFF7FAFC),
    surface = Color.White,
)

private val DarkColors = darkColorScheme(
    primary = HpBlue,
    onPrimary = Color.White,
    primaryContainer = HpDark,
    onPrimaryContainer = HpLight,
    secondary = HpLight,
    background = Color(0xFF0E1418),
    surface = Color(0xFF142028),
)

@Composable
fun HPPrinterTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = if (darkTheme) DarkColors else LightColors,
        content = content
    )
}
