import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from ai_engine.services import generate_ai_remedy, parse_ai_remedy_payload
from remedies.models import AIConsultation


class AIConsultationFlowTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='tester',
			email='tester@example.com',
			password='pass12345'
		)
		self.client.login(username='tester', password='pass12345')

	def test_generate_ai_remedy_returns_json_payload(self):
		payload_text = generate_ai_remedy(
			'I have acne and oily skin with redness',
			'honey, aloe vera, turmeric, lemon',
			self.user,
		)

		parsed = json.loads(payload_text)
		self.assertIn('ingredients', parsed)
		self.assertIn('instructions', parsed)
		self.assertIn('benefits', parsed)
		self.assertIn('precautions', parsed)
		self.assertEqual(parsed.get('generation_source'), 'unavailable')

	def test_parse_ai_remedy_payload_handles_legacy_text(self):
		legacy = 'Old plain text remedy output\nLine two'
		parsed = parse_ai_remedy_payload(legacy)

		self.assertEqual(parsed['generation_source'], 'legacy')
		self.assertIn('Old plain text remedy output', parsed['legacy_text'])

	def test_consultation_detail_renders_structured_sections(self):
		payload_text = generate_ai_remedy(
			'I have dry skin and rough patches',
			'yogurt, honey, aloe vera',
			self.user,
		)
		consultation = AIConsultation.objects.create(
			user=self.user,
			problem_description='I have dry skin and rough patches',
			available_ingredients='yogurt, honey, aloe vera',
			suggested_remedy=payload_text,
		)

		response = self.client.get(reverse('consultation_detail', args=[consultation.id]))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Ingredients')
		self.assertContains(response, 'Preparation Instructions')
		self.assertContains(response, 'How to Use')
		self.assertContains(response, 'Precautions')

	def test_ai_consultation_post_shows_error_and_does_not_save_when_ai_unavailable(self):
		response = self.client.post(
			reverse('ai_consultation'),
			{
				'problem_description': 'Menstrual cramps',
				'available_ingredients': 'ginger, warm water',
			},
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Live AI is not available')
		self.assertEqual(AIConsultation.objects.filter(user=self.user).count(), 0)
