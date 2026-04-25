package printer.smart.app.ui

import android.graphics.Bitmap
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun HomeScreen() {
    val context = LocalContext.current

    // Photo picker — system-managed, needs no permission.
    val pickImage = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        uri?.let { Actions.printImageUri(context, it, "Print Photo") }
    }

    // Document picker — SAF, needs no permission.
    val pickDocument = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.OpenDocument()
    ) { uri: Uri? ->
        uri?.let { Actions.openDocumentForPrinting(context, it) }
    }

    // Camera — system intent, needs NO runtime permission as long as the
    // app does not declare CAMERA in the manifest.
    val captureSimple = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.TakePicturePreview()
    ) { bitmap: Bitmap? ->
        bitmap?.let { Actions.printBitmap(context, it, "Photocopy") }
    }

    // ID card — two-step capture. State persists across taps of the tile.
    val idCardFirst = remember { mutableStateOf<Bitmap?>(null) }
    val captureIdCard = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.TakePicturePreview()
    ) { bitmap: Bitmap? ->
        if (bitmap == null) return@rememberLauncherForActivityResult
        val first = idCardFirst.value
        if (first == null) {
            idCardFirst.value = bitmap
            Actions.toast(context, "Front captured. Tap ID Card again for the back.")
        } else {
            val combined = Actions.stackVertically(first, bitmap)
            idCardFirst.value = null
            Actions.printBitmap(context, combined, "ID Card Copy")
        }
    }

    val onTool: (Tool) -> Unit = { tool ->
        when (tool.action) {
            ToolAction.PrintPhoto -> Actions.safe(context) { pickImage.launch("image/*") }
            ToolAction.PrintPdf -> Actions.safe(context) {
                pickDocument.launch(
                    arrayOf(
                        "application/pdf",
                        "image/*",
                        "application/msword",
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )
                )
            }
            ToolAction.ScanDocument,
            ToolAction.Photocopy -> Actions.safe(context) { captureSimple.launch(null) }
            ToolAction.IdCardCopy -> Actions.safe(context) { captureIdCard.launch(null) }
            ToolAction.MobileFax -> Actions.sendFaxEmail(context)
            ToolAction.FindPrinter -> Actions.openWifiSettings(context)
            ToolAction.PrintServicesSettings -> Actions.openPrintServices(context)
            is ToolAction.OpenUrl -> Actions.openUrl(context, tool.action.url)
            ToolAction.PrintWebPage -> Actions.openUrl(context, "https://www.google.com")
            ToolAction.InstallPrintPlugin -> Actions.openPlayStorePage(
                context, "com.hp.android.printservice"
            )
            ToolAction.AppSettings -> Actions.openAppSettings(context)
        }
    }

    Column(modifier = Modifier.fillMaxSize()) {
        Header()
        LazyVerticalGrid(
            columns = GridCells.Fixed(2),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            modifier = Modifier.fillMaxSize()
        ) {
            items(Tools.all, key = { it.id }) { tool ->
                ToolCard(tool = tool, onClick = { onTool(tool) })
            }
        }
    }
}

@Composable
private fun Header() {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .background(
                Brush.horizontalGradient(
                    listOf(
                        MaterialTheme.colorScheme.primary,
                        MaterialTheme.colorScheme.secondary,
                    )
                )
            )
            .padding(horizontal = 20.dp, vertical = 24.dp)
    ) {
        Column {
            Text(
                text = "Smart Print Tools",
                color = MaterialTheme.colorScheme.onPrimary,
                fontWeight = FontWeight.Bold,
                fontSize = 26.sp,
            )
            Spacer(Modifier.height(4.dp))
            Text(
                text = "Tap a tool to start",
                color = MaterialTheme.colorScheme.onPrimary,
                fontSize = 14.sp,
            )
        }
    }
}

@Composable
private fun ToolCard(tool: Tool, onClick: () -> Unit) {
    Card(
        onClick = onClick,
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
        modifier = Modifier
            .fillMaxWidth()
            .aspectRatio(1f)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(14.dp),
            verticalArrangement = Arrangement.SpaceBetween,
        ) {
            Box(
                modifier = Modifier
                    .size(44.dp)
                    .clip(RoundedCornerShape(12.dp))
                    .background(MaterialTheme.colorScheme.primaryContainer),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = tool.icon,
                    contentDescription = tool.title,
                    tint = MaterialTheme.colorScheme.onPrimaryContainer
                )
            }
            Column {
                Text(
                    text = tool.title,
                    fontWeight = FontWeight.SemiBold,
                    fontSize = 15.sp,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
                Text(
                    text = tool.subtitle,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f),
                    fontSize = 12.sp,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
            }
        }
    }
}
