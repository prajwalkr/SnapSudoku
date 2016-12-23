package com.example.yash.snapsudoku.network;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Query;

/**
 * Created by Yash on 12/23/2016.
 */
public interface SudokuService {

    @GET(".")
    Call<String> getIndex();
}