package com.example.yash.snapsudoku;

import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.widget.ImageView;
import android.widget.Toast;

import com.example.yash.snapsudoku.network.SudokuService;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.scalars.ScalarsConverterFactory;

public class MainActivity extends AppCompatActivity {

    public static final int REQUEST_CODE = 101;

    private ImageView ivPhoto;
    private Bitmap imageBitmap = null;

    private SudokuService service;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ivPhoto = (ImageView) findViewById(R.id.ivPhoto);

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://10.0.2.2:8000/")
                .addConverterFactory(ScalarsConverterFactory.create())
                .build();
        service = retrofit.create(SudokuService.class);

        Intent intentTakePhoto = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        startActivityForResult(intentTakePhoto, REQUEST_CODE);
    }

    @Override
    protected void onActivityResult(int requestCode, final int resultCode, Intent data) {
        if (requestCode == REQUEST_CODE && resultCode == RESULT_OK) {
            imageBitmap = (Bitmap) data.getExtras().get("data");

            ivPhoto.setImageBitmap(imageBitmap);
            saveTempBitmap();

            File f = getCachedBitmap();
            RequestBody requestBody = RequestBody.create(MediaType.parse("image/jpeg"), f);
            MultipartBody.Part image = MultipartBody.Part.createFormData("image", f.getName(), requestBody);

            solveSudoku(image);
        }
    }

    private void solveSudoku(MultipartBody.Part image) {
        service.solveSudoku(image)
                .enqueue(new Callback<String>() {
                    @Override
                    public void onResponse(Call<String> call, Response<String> response) {
                        Toast.makeText(MainActivity.this, response.body(), Toast.LENGTH_SHORT).show();
                    }

                    @Override
                    public void onFailure(Call<String> call, Throwable t) {
                        Toast.makeText(MainActivity.this, "Wrong", Toast.LENGTH_SHORT).show();
                    }
                });
    }

    @NonNull
    private File getCachedBitmap() {
        File cacheDir = getBaseContext().getCacheDir();
        return new File(cacheDir, getString(R.string.image_file_name));
    }

    private void saveTempBitmap() {
        File cacheDir = getBaseContext().getCacheDir();
        File f = new File(cacheDir, getString(R.string.image_file_name));

        try {
            FileOutputStream out = new FileOutputStream(f);
            imageBitmap.compress(Bitmap.CompressFormat.PNG, 100, out);
            out.flush();
            out.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
