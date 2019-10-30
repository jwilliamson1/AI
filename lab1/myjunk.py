
from production import IF, AND, OR, NOT, THEN, DELETE, forward_chain
theft_rule = IF( 'you have (?x)',
 THEN( 'i have (?x)' ),
 DELETE( 'you have (?x)' ))
return_rule = IF( 'i have (?x)',
 THEN( 'they have (?x)' ),
 DELETE( 'i have (?x)' ))
data = ( 'you have apple',
 'you have orange',
 'you have pear' )
print forward_chain([theft_rule, return_rule], data, verbose=True) 
