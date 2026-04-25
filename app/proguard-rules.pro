# --- Compose / AndroidX ---
-keepclasseswithmembers class * {
    @androidx.compose.runtime.Composable <methods>;
}
-dontwarn org.jetbrains.annotations.**
-dontwarn kotlin.**

# --- Kotlinx Serialization (none used today, but harmless) ---
-keepattributes *Annotation*, InnerClasses
-dontnote kotlinx.serialization.SerializationKt

# --- Keep enum / Parcelable signatures used by intents ---
-keepclassmembers enum * { *; }
-keepclassmembers class * implements android.os.Parcelable {
    public static final ** CREATOR;
}

# --- Keep app entry points ---
-keep class printer.smart.app.MainActivity { *; }
