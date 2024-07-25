(define (make-adder num) (lambda (x) (+ num x)))

(define (composed f g) (lambda (x)(f (g x))))

(define (my-filter pred s) (if (null? s) '() (if (pred (car s)) (cons (car s) (my-filter pred (cdr s))) (my-filter pred (cdr s)))))

(define (exp b n)
  (define (helper b n so-far)(if (= n 0)so-far(helper b ( - n 1)(* b so-far))))(helper b n 1))

(define (interleave lst1 lst2) 'YOUR-CODE-HERE)

(define (square n) (* n n))

(define (pow base exp) 'YOUR-CODE-HERE)
