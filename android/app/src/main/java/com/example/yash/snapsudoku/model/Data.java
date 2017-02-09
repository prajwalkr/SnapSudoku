package com.example.yash.snapsudoku.model;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Data {

    @SerializedName("solution")
    @Expose
    private List<List<Integer>> solution = null;

    public List<List<Integer>> getSolution() {
        return solution;
    }

    public void setSolution(List<List<Integer>> solution) {
        this.solution = solution;
    }

}