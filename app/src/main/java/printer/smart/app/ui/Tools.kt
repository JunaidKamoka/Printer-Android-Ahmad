package printer.smart.app.ui

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AssignmentInd
import androidx.compose.material.icons.filled.CameraAlt
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.DocumentScanner
import androidx.compose.material.icons.filled.Email
import androidx.compose.material.icons.filled.Extension
import androidx.compose.material.icons.filled.Image
import androidx.compose.material.icons.filled.Language
import androidx.compose.material.icons.filled.PictureAsPdf
import androidx.compose.material.icons.filled.Print
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.WaterDrop
import androidx.compose.material.icons.filled.Wifi
import androidx.compose.ui.graphics.vector.ImageVector

data class Tool(
    val id: String,
    val title: String,
    val subtitle: String,
    val description: String,
    val icon: ImageVector,
    val action: ToolAction,
)

sealed interface ToolAction {
    data object PrintPhoto : ToolAction
    data object PrintPdf : ToolAction
    data object ScanDocument : ToolAction
    data object Photocopy : ToolAction
    data object IdCardCopy : ToolAction
    data object MobileFax : ToolAction
    data object FindPrinter : ToolAction
    data object PrintServicesSettings : ToolAction
    data class OpenUrl(val url: String) : ToolAction
    data object PrintWebPage : ToolAction
    data object InstallPrintPlugin : ToolAction
    data object AppSettings : ToolAction
}

object Tools {
    val all: List<Tool> = listOf(
        Tool(
            id = "print_photo",
            title = "Print Photo",
            subtitle = "From gallery",
            description = "Pick a picture from your gallery and send it to the printer.",
            icon = Icons.Filled.Image,
            action = ToolAction.PrintPhoto,
        ),
        Tool(
            id = "print_pdf",
            title = "Print Document",
            subtitle = "PDF, DOCX, etc.",
            description = "Choose a document file and print it through your HP printer.",
            icon = Icons.Filled.PictureAsPdf,
            action = ToolAction.PrintPdf,
        ),
        Tool(
            id = "scan",
            title = "Scan Document",
            subtitle = "Use camera",
            description = "Capture a page with the camera, then save or print the result.",
            icon = Icons.Filled.DocumentScanner,
            action = ToolAction.ScanDocument,
        ),
        Tool(
            id = "photocopy",
            title = "Photocopy",
            subtitle = "Capture & print",
            description = "Take a quick photo of a page and immediately print a copy.",
            icon = Icons.Filled.ContentCopy,
            action = ToolAction.Photocopy,
        ),
        Tool(
            id = "id_copy",
            title = "ID Card Copy",
            subtitle = "Front & back",
            description = "Capture both sides of an ID card and print them on a single page.",
            icon = Icons.Filled.AssignmentInd,
            action = ToolAction.IdCardCopy,
        ),
        Tool(
            id = "fax",
            title = "Mobile Fax",
            subtitle = "Send by email",
            description = "Compose a fax-style email with an attachment to send from your phone.",
            icon = Icons.Filled.Email,
            action = ToolAction.MobileFax,
        ),
        Tool(
            id = "find_printer",
            title = "Find Printer",
            subtitle = "Wi-Fi setup",
            description = "Open Wi-Fi settings to connect to your HP printer's network.",
            icon = Icons.Filled.Wifi,
            action = ToolAction.FindPrinter,
        ),
        Tool(
            id = "printer_status",
            title = "Printer Status",
            subtitle = "Print services",
            description = "Check the Android print services to see your printer's status.",
            icon = Icons.Filled.Print,
            action = ToolAction.PrintServicesSettings,
        ),
        Tool(
            id = "ink_levels",
            title = "Ink Levels",
            subtitle = "Check supplies",
            description = "Open the HP supplies page to view ink and toner levels for your printer.",
            icon = Icons.Filled.WaterDrop,
            action = ToolAction.OpenUrl("https://www.hp.com/us-en/shop/cat/ink-toner"),
        ),
        Tool(
            id = "setup",
            title = "Setup Printer",
            subtitle = "123.hp.com",
            description = "Walk through the official HP setup flow at 123.hp.com.",
            icon = Icons.Filled.CameraAlt,
            action = ToolAction.OpenUrl("https://123.hp.com/setup"),
        ),
        Tool(
            id = "web_print",
            title = "Print Web Page",
            subtitle = "From browser",
            description = "Open a website and print it directly from the browser menu.",
            icon = Icons.Filled.Language,
            action = ToolAction.PrintWebPage,
        ),
        Tool(
            id = "plugin",
            title = "HP Print Plugin",
            subtitle = "Play Store",
            description = "Install or update the HP Print Service Plugin to print to HP printers.",
            icon = Icons.Filled.Extension,
            action = ToolAction.InstallPrintPlugin,
        ),
        Tool(
            id = "settings",
            title = "App Settings",
            subtitle = "Permissions",
            description = "Open this app's system settings to manage permissions.",
            icon = Icons.Filled.Settings,
            action = ToolAction.AppSettings,
        ),
    )

    fun byId(id: String): Tool? = all.firstOrNull { it.id == id }
}
