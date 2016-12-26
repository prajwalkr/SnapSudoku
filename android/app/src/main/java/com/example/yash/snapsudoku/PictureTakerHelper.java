package com.example.yash.snapsudoku;

import android.content.Context;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.media.ExifInterface;
import android.net.Uri;
import android.provider.MediaStore;
import android.util.Base64;
import android.util.Log;

import java.io.ByteArrayOutputStream;

/*
This class can be used for phones which rotate images when clicked
 */
public class PictureTakerHelper {

    public static Bitmap rotateBitmapIfNeeded(String absolutePath, Bitmap bitmap) {
        Bitmap result = bitmap;
        try {
            ExifInterface ei = new ExifInterface(absolutePath);
            int orientation = ei.getAttributeInt(ExifInterface.TAG_ORIENTATION,
                    ExifInterface.ORIENTATION_NORMAL);

            switch (orientation) {
                case ExifInterface.ORIENTATION_ROTATE_90:
                    result = rotateBitmap(bitmap, 90);
                    break;
                case ExifInterface.ORIENTATION_ROTATE_180:
                    result = rotateBitmap(bitmap, 180);
                    break;
                case ExifInterface.ORIENTATION_ROTATE_270:
                    result = rotateBitmap(bitmap, 270);
                    break;
            }
        } catch (Exception e) {
            Log.d("Camera", e.getMessage());
        }

        return result;
    }

    public static Bitmap rotateBitmap(Bitmap source, float angle) {
        Matrix matrix = new Matrix();
        matrix.postRotate(angle);
        return Bitmap.createBitmap(source, 0, 0, source.getWidth(),
                source.getHeight(), matrix, true);
    }

    public static String getAbsolutePathBy(Context context, Uri uri) {
        String[] filePathColumn = {MediaStore.Images.Media.DATA};

        Cursor cursor = context.getContentResolver().query(uri, filePathColumn,
                null, null, null);
        cursor.moveToFirst();
        int columnIndex = cursor.getColumnIndex(filePathColumn[0]);
        String picturePath = cursor.getString(columnIndex);
        cursor.close();
        return picturePath;
    }

    public static String getPhotoBase64(String photoPath) {
        if (photoPath != null && !"".equals(photoPath)) {
            BitmapFactory.Options options = new BitmapFactory.Options();
            options.inSampleSize = 4;
            Bitmap original = BitmapFactory.decodeFile(photoPath, options);
            Bitmap resized = Bitmap.createScaledBitmap(original, 1280, 800,
                    true);

            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            resized.compress(Bitmap.CompressFormat.JPEG, 80, baos);

            String encodedImage = Base64.encodeToString(baos.toByteArray(),
                    Base64.DEFAULT);

            original.recycle();
            resized.recycle();
            return encodedImage;
        } else {
            return "";
        }
    }

}