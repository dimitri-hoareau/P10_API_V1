from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from api_tracking_system.models import Project

class Testproject(APITestCase):
    # Nous stockons l’url de l'endpoint dans un attribut de classe pour pouvoir l’utiliser plus facilement dans chacun de nos tests
    url = reverse_lazy('project-list')

    def test_list(self):
        # Créons deux catégories dont une seule est active


        project = Project.objects.create(title='project1', author=1, )
        Project.objects.create(title='project2')

        # On réalise l’appel en GET en utilisant le client de la classe de test
        response = self.client.get(self.url)
        # Nous vérifions que le status code est bien 200
        # et que les valeurs retournées sont bien celles attendues
        self.assertEqual(response.status_code, 200)
        excepted = [
            {
                'id': project.pk,
                'title': project.title,
                'description' : project.description,
                'type' : project.type,
                'author' : project.author
            }
        ]
        self.assertEqual(excepted, response.json())

    # def test_create(self):
    #     # Nous vérifions qu’aucune catégorie n'existe avant de tenter d’en créer une
    #     self.assertFalse(Project.objects.exists())
    #     response = self.client.post(self.url, data={'title': 'Nouveaux projet'})
    #     # Vérifions que le status code est bien en erreur et nous empêche de créer une catégorie
    #     self.assertEqual(response.status_code, 405)
    #     # Enfin, vérifions qu'aucune nouvelle catégorie n’a été créée malgré le status code 405
    #     self.assertFalse(Project.objects.exists())



    #setup, créer des données en amont
    #pour le test créer l'user