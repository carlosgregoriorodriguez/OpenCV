import pyopencl as cl
import numpy
import numpy.linalg as la
import time

a = numpy.random.rand(5000000).astype(numpy.float64)
b = numpy.random.rand(5000000).astype(numpy.float64)

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

mf = cl.mem_flags
prg = cl.Program(ctx, """
    __kernel void sum(__global const float *a,
    __global const float *b, __global float *c)
    {
      int gid = get_global_id(0);
      c[gid] = a[gid] + b[gid];
    }
    """).build()

def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
        return res
    return wrapper

a_plus_b = numpy.empty_like(a)

def bench():

	a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
	b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
	dest_buf = cl.Buffer(ctx, mf.WRITE_ONLY, b.nbytes)
	prg.sum(queue, a.shape, None, a_buf, b_buf, dest_buf)
	return dest_buf
	# cl.enqueue_copy(queue, a_plus_b, dest_buf)
	# return a_plus_b

def bench_numpy():
	return a+b

print 'Opencl', print_timing(bench)()
print 'Numpy', print_timing(bench_numpy)()

# print la.norm(a_plus_b - (a+b))
