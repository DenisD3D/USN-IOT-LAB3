<?php

use Illuminate\Support\Facades\Route;
use App\LaravelChart;
/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

Route::get('/', function () {
    return redirect(config('fortify.home'));
});

Route::middleware([
    'auth:sanctum',
    config('jetstream.auth_session'),
    'verified',
])->group(function () {
    Route::get('/dashboard', function () {
        $chart_options = [
            'chart_title' => 'Air Heater Temperature',
            'report_type' => 'group_by_date',
            'model' => 'App\Models\Temperature',
            'group_by_field' => 'created_at',
            'group_by_period' => 'second',
            'chart_type' => 'line',
            'aggregate_function' => 'avg',
            'aggregate_field' => 'temperature',
            'chart_color' => '104,117,245'
        ];
        $chart1 = new LaravelChart($chart_options);
        return view('dashboard', compact('chart1'));
    })->name('dashboard');
});
