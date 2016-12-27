package com.example.yash.snapsudoku.model;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class SudokuSolution {

    @SerializedName("success")
    @Expose
    private String success;
    @SerializedName("data")
    @Expose
    private Data data;
    @SerializedName("error")
    @Expose
    private Error error;

    public String getSuccess() {
        return success;
    }

    public void setSuccess(String success) {
        this.success = success;
    }

    public Data getData() {
        return data;
    }

    public void setData(Data data) {
        this.data = data;
    }

    public Error getError() {
        return error;
    }

    public void setError(Error error) {
        this.error = error;
    }
}