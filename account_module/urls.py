from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register_view'),
    path('login/', views.LoginView.as_view(), name='login_view'),
    path('logout/', views.LogoutView.as_view(), name='logout_view'),
    path('user-panel/', views.UserPanel.as_view(), name='user_panel_view'),
    path('user-panel/edit-info/', views.EditUserInfoView.as_view(), name='edit_user_info_view'),
    path('user-panel/edit-password/', views.EditUserPasswordView.as_view(), name='edit_user_password_view'),
    path('order-history/', views.OrderHistoryView.as_view(), name='order_history_view'),
    path('order-history/pdf/<int:order_id>/', views.OrderHistoryExportView.as_view(), name='order_history_export_view'),
    path('api/v1/', include('account_module.api.v1.urls')),
]
