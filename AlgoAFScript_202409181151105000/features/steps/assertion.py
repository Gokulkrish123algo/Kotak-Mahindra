def assert_equal(context, actual, expected, message=None):
	"""this method compare the actual and excepted value"""
	if str(context.softAssertion).lower() == 'true':
		try:
			assert actual == expected, message
			step_name = str(context.current_step.name)
			status = 'true'
			failure_info = {'name': step_name, 'status': status}
			context.softFailurelist.append(failure_info)
		except AssertionError:
			step_name = str(context.current_step.name)
			status = 'false'
			failure_info = {'name': step_name, 'status': status}
			context.softFailurelist.append(failure_info)
	else:
		assert actual == expected, message


def assert_true(context, condition, message=None):
	"""this method compare true of false"""
	if str(context.softAssertion).lower() == 'true':
		try:
			assert condition, message
			step_name = str(context.current_step.name)
			status = 'true'
			failure_info = {'name': step_name, 'status': status}
			context.softFailurelist.append(failure_info)
		except AssertionError:
			step_name = str(context.current_step.name)
			status = 'false'
			failure_info = {'name': step_name, 'status': status}
			context.softFailurelist.append(failure_info)
	else:
		assert condition, message


def assert_false(context, condition, message=None):
	"""this method compare true of false"""
	if str(context.softAssertion).lower() == 'true':
		try:
			assert not condition, message
			step_name = str(context.current_step.name)
			status = 'true'
			failure_info = {'name': step_name, 'status': status}
			context.softFailurelist.append(failure_info)
		except AssertionError:
			step_name = str(context.current_step.name)
			status = 'false'
			failure_info = {'name': step_name, 'status': status}
			context.softFailurelist.append(failure_info)
	else:
		assert condition, message


def assert_all(context, message=None):
	"""this method at the end of the statement it will throws exception"""
	for step_info in context.softFailurelist:
		step_name = step_info['name']
		if step_info['status'] == 'false':  # Corrected from 'false' to 'failed'
			raise Exception('Failed in step: {}'.format(step_name))
	assert True


