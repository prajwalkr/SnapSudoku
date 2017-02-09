package com.example.yash.snapsudoku.network;

import com.example.yash.snapsudoku.model.SudokuSolution;

import okhttp3.MultipartBody;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;
import retrofit2.http.Query;

/**
 * Created by Yash on 12/23/2016.
 */
public interface SudokuService {

    @GET(".")
    Call<String> getIndex();

    @Multipart
    @POST(" sudoku/solve/")
    Call<SudokuSolution> solveSudoku(@Part MultipartBody.Part image);
}