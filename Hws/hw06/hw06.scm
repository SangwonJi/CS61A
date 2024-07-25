(define (no-repeats lst)
    (if (null? lst)
        '()
        (let ((rest (filter (lambda (x) (not ( = x (car lst))))(cdr lst))))
        (cons (car lst) (no-repeats rest)))))
        
(define (student-attend-class student class)
  (let(( name (student-get-name student)) (classes(student-get-classes student)))
  (student-create name (cons class classes))))

(define (teacher-hold-class teacher)
  (teacher-create( teacher-get-name teacher) (teacher-get-class teacher)
  (map (lambda (student) (student-attend-class student (teacher-get-class teacher)))(teacher-get-students teacher))))

(define (add-leaf t x)
  (if (is-leaf t)
      t
      (begin (define mapped-branches
                     (map (lambda(branch) (add-leaf branch x)) (branches t)))
             (tree (label t)
                   (append mapped-branches (list(tree x nil)))))))
