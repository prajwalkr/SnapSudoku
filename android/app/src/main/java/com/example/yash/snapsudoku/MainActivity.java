package com.example.yash.snapsudoku;

import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.ImageView;
import android.widget.Toast;

import com.example.yash.snapsudoku.model.SudokuSolution;
import com.example.yash.snapsudoku.network.SudokuService;

import java.io.File;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class MainActivity extends AppCompatActivity {

    public static final int REQUEST_CODE = 101;
    public static final String LOG_TAG = "LOG_TAG";

    private ImageView ivPhoto;
    private Bitmap imageBitmap = null;

    private SudokuService service;
    private String path;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ivPhoto = (ImageView) findViewById(R.id.ivPhoto);

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://10.0.2.2:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();
        service = retrofit.create(SudokuService.class);

        path = Environment.getExternalStorageDirectory() + "/image.jpg";

        Intent intentTakePhoto = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        intentTakePhoto.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(new File(path)));
        startActivityForResult(intentTakePhoto, REQUEST_CODE);
    }

    @Override
    protected void onActivityResult(int requestCode, final int resultCode, Intent data) {
        if (requestCode == REQUEST_CODE && resultCode == RESULT_OK) {

            File f = new File(path);
            RequestBody requestBody = RequestBody.create(MediaType.parse("image/jpeg"), f);
            MultipartBody.Part image = MultipartBody.Part.createFormData("image", f.getName(), requestBody);

            solveSudoku(image);
        }
    }

    private void solveSudoku(MultipartBody.Part image) {
        service.solveSudoku(image)
                .enqueue(new Callback<SudokuSolution>() {
                    @Override
                    public void onResponse(Call<SudokuSolution> call, Response<SudokuSolution> response) {
                        Log.v(LOG_TAG, response.body().toString());
                    }

                    @Override
                    public void onFailure(Call<SudokuSolution> call, Throwable t) {
                        Toast.makeText(MainActivity.this, t.getMessage(), Toast.LENGTH_SHORT).show();
                    }
                });
    }
}
