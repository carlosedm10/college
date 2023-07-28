transcript on
if {[file exists gate_work]} {
	vdel -lib gate_work -all
}
vlib gate_work
vmap work gate_work

vlog -vlog01compat -work work +incdir+. {motor_7_1200mv_85c_slow.vo}

vlog -vlog01compat -work work +incdir+W:/SDP/Prac3 {W:/SDP/Prac3/control_motor_tb.v}

vsim -t 1ps +transport_int_delays +transport_path_delays -L altera_ver -L cycloneive_ver -L gate_work -L work -voptargs="+acc"  control_motor_tb

add wave *
view structure
view signals
run -all
