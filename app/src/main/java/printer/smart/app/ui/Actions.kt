package printer.smart.app.ui

import android.app.Activity
import android.content.ActivityNotFoundException
import android.content.ClipData
import android.content.Context
import android.content.ContextWrapper
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Paint
import android.net.Uri
import android.provider.Settings
import android.util.Log
import android.widget.Toast
import androidx.core.net.toUri
import androidx.print.PrintHelper

internal const val TAG = "PrinterTools"

object Actions {

    /** Run a block but turn any exception into a user-visible toast instead of a crash. */
    fun safe(context: Context, block: () -> Unit) {
        try {
            block()
        } catch (t: Throwable) {
            Log.w(TAG, "action failed", t)
            toast(context, "Could not open this tool: ${t.message ?: "unknown error"}")
        }
    }

    fun toast(context: Context, msg: String) {
        Toast.makeText(context, msg, Toast.LENGTH_SHORT).show()
    }

    // ---------- printing ----------

    fun printBitmap(context: Context, bitmap: Bitmap, jobName: String) {
        val activity = context.findActivity()
        if (activity == null) {
            toast(context, "Cannot print from this screen")
            return
        }
        try {
            PrintHelper(activity).apply {
                scaleMode = PrintHelper.SCALE_MODE_FIT
                colorMode = PrintHelper.COLOR_MODE_COLOR
                orientation = PrintHelper.ORIENTATION_PORTRAIT
            }.printBitmap(jobName, bitmap)
        } catch (t: Throwable) {
            Log.w(TAG, "printBitmap failed", t)
            toast(context, "Could not print: ${t.message ?: "no printer service"}")
        }
    }

    fun printImageUri(context: Context, uri: Uri, jobName: String) {
        val activity = context.findActivity()
        if (activity == null) {
            toast(context, "Cannot print from this screen")
            return
        }
        try {
            PrintHelper(activity).apply {
                scaleMode = PrintHelper.SCALE_MODE_FIT
                colorMode = PrintHelper.COLOR_MODE_COLOR
            }.printBitmap(jobName, uri)
        } catch (t: Throwable) {
            Log.w(TAG, "printImageUri failed", t)
            toast(context, "Could not print image: ${t.message ?: "unknown error"}")
        }
    }

    /** Opens the chosen document in any viewer; user can use that app's Print menu. */
    fun openDocumentForPrinting(context: Context, uri: Uri) {
        val mime = context.contentResolver.getType(uri) ?: "application/octet-stream"
        val intent = Intent(Intent.ACTION_VIEW).apply {
            setDataAndType(uri, mime)
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            // Carry the URI grant through any chooser the system shows.
            clipData = ClipData.newRawUri("", uri)
        }
        try {
            context.startActivity(intent)
            toast(context, "Use the Print option in the menu to send to your printer.")
        } catch (e: ActivityNotFoundException) {
            toast(context, "No app installed to view this file.")
        } catch (t: Throwable) {
            Log.w(TAG, "openDocumentForPrinting failed", t)
            toast(context, "Could not open document.")
        }
    }

    // ---------- intents ----------

    fun openUrl(context: Context, url: String) {
        try {
            context.startActivity(
                Intent(Intent.ACTION_VIEW, url.toUri())
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            )
        } catch (e: ActivityNotFoundException) {
            toast(context, "No browser installed.")
        } catch (t: Throwable) {
            Log.w(TAG, "openUrl failed", t)
            toast(context, "Cannot open: $url")
        }
    }

    fun openPlayStorePage(context: Context, packageName: String) {
        // Prefer the Play Store app; fall back to the web URL.
        val marketIntent = Intent(
            Intent.ACTION_VIEW, "market://details?id=$packageName".toUri()
        ).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        try {
            context.startActivity(marketIntent)
        } catch (e: ActivityNotFoundException) {
            openUrl(context, "https://play.google.com/store/apps/details?id=$packageName")
        }
    }

    fun openWifiSettings(context: Context) {
        try {
            context.startActivity(
                Intent(Settings.ACTION_WIFI_SETTINGS).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            )
        } catch (t: Throwable) {
            Log.w(TAG, "openWifiSettings failed", t)
            openAppSettings(context)
        }
    }

    /** Best-effort: try the (hidden) print-services screen, then fall back to system settings. */
    fun openPrintServices(context: Context) {
        val candidates = listOf(
            Intent("android.settings.ACTION_PRINT_SETTINGS"),
            Intent(Settings.ACTION_SETTINGS),
        )
        for (intent in candidates) {
            try {
                context.startActivity(intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
                return
            } catch (_: Throwable) { /* try next */ }
        }
        toast(context, "Settings unavailable on this device.")
    }

    fun openAppSettings(context: Context) {
        try {
            context.startActivity(
                Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS)
                    .setData("package:${context.packageName}".toUri())
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            )
        } catch (t: Throwable) {
            Log.w(TAG, "openAppSettings failed", t)
            toast(context, "Cannot open app settings.")
        }
    }

    fun sendFaxEmail(context: Context) {
        val intent = Intent(Intent.ACTION_SENDTO).apply {
            data = "mailto:".toUri()
            putExtra(Intent.EXTRA_SUBJECT, "Mobile Fax")
            putExtra(Intent.EXTRA_TEXT, "Please find the attached document.")
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        try {
            context.startActivity(intent)
        } catch (e: ActivityNotFoundException) {
            toast(context, "No email app installed.")
        } catch (t: Throwable) {
            Log.w(TAG, "sendFaxEmail failed", t)
            toast(context, "Could not open email app.")
        }
    }

    // ---------- utilities ----------

    /** Walk the Context wrapper chain to find the hosting Activity. */
    fun Context.findActivity(): Activity? {
        var ctx: Context? = this
        while (ctx is ContextWrapper) {
            if (ctx is Activity) return ctx
            ctx = ctx.baseContext
        }
        return null
    }

    fun stackVertically(top: Bitmap, bottom: Bitmap): Bitmap {
        val width = maxOf(top.width, bottom.width)
        val gap = 24
        val height = top.height + bottom.height + gap
        val out = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888)
        val canvas = Canvas(out)
        canvas.drawColor(android.graphics.Color.WHITE)
        val paint = Paint(Paint.FILTER_BITMAP_FLAG)
        canvas.drawBitmap(top, ((width - top.width) / 2f), 0f, paint)
        canvas.drawBitmap(bottom, ((width - bottom.width) / 2f), (top.height + gap).toFloat(), paint)
        return out
    }
}
